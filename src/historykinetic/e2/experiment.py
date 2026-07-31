from __future__ import annotations

from collections import Counter
from statistics import mean

from historykinetic.e2.models import (
    CalibrationDoseRow,
    E2BranchAudit,
    E2BranchRun,
    E2CalibrationResult,
    E2CaseResult,
    E2Direction,
    E2MetricRow,
    E2StudyResult,
)
from historykinetic.e2.protocol import MolecularEchoesE2Protocol, MoleculeBudget
from historykinetic.echo import (
    PassiveColorMap,
    color_score,
    prepare_echo_initial_state,
    reverse_state,
)
from historykinetic.molecules import (
    EncounterDecision,
    FullCollisionPolicy,
    GhostCollisionPolicy,
    MoleculeBudgetPolicy,
    QuotaMatchedRandomPolicy,
    TopologyShuffledBudgetPolicy,
)
from historykinetic.molecules.models import EncounterEvent, ModifiedSimulationResult
from historykinetic.solvers import (
    DiskState,
    HardDiskEDMD,
    ModifiedHardDiskEDMD,
    SimulationResult,
)


def run_e2(protocol: MolecularEchoesE2Protocol) -> E2StudyResult:
    cases = tuple(
        _run_case(protocol, particle_count=size.count, seed=seed)
        for size in protocol.e1_protocol.sizes
        for seed in protocol.seeds
    )
    return E2StudyResult(protocol=protocol, cases=cases)


def calibrate_e2_budget(protocol: MolecularEchoesE2Protocol) -> E2CalibrationResult:
    rows: list[CalibrationDoseRow] = []
    for seed in protocol.calibration_seeds:
        _initial, _colors, _preparation, pivot = _prepare_case(
            protocol,
            particle_count=protocol.calibration_particle_count,
            seed=seed,
        )
        for direction in E2Direction:
            branch_state = (
                pivot.copy()
                if direction is E2Direction.FORWARD
                else reverse_state(pivot)
            )
            full = _run_policy(protocol, branch_state, FullCollisionPolicy())
            full_count = len(full.accepted_encounters)
            for budget in protocol.budgets:
                result = _run_policy(
                    protocol,
                    branch_state,
                    MoleculeBudgetPolicy(
                        budget.maximum_component_size,
                        budget.maximum_cycle_rank,
                    ),
                )
                accepted = len(result.accepted_encounters)
                rows.append(
                    CalibrationDoseRow(
                        seed=seed,
                        direction=direction,
                        branch=budget.branch_name,
                        accepted_collision_count=accepted,
                        full_collision_count=full_count,
                        collision_dose=accepted / max(full_count, 1),
                    )
                )
    dose_by_branch = {
        budget.branch_name: mean(
            row.collision_dose for row in rows if row.branch == budget.branch_name
        )
        for budget in protocol.budgets
    }
    selected = min(dose_by_branch, key=lambda name: (abs(dose_by_branch[name] - 0.5), name))
    return E2CalibrationResult(protocol=protocol, rows=tuple(rows), selected_branch=selected)


def _run_case(
    protocol: MolecularEchoesE2Protocol,
    *,
    particle_count: int,
    seed: int,
) -> E2CaseResult:
    initial, colors, preparation, pivot = _prepare_case(
        protocol,
        particle_count=particle_count,
        seed=seed,
    )
    pivot_score = color_score(pivot, colors, protocol.e1_protocol)
    branches: list[E2BranchRun] = []
    metrics: list[E2MetricRow] = []
    audits: list[E2BranchAudit] = []
    for direction in E2Direction:
        branch_state = pivot.copy() if direction is E2Direction.FORWARD else reverse_state(pivot)
        direction_runs: list[tuple[str, ModifiedSimulationResult]] = []
        ghost = _run_policy(protocol, branch_state, GhostCollisionPolicy())
        direction_runs.append(("ghost", ghost))
        structured: dict[MoleculeBudget, ModifiedSimulationResult] = {}
        for budget in protocol.budgets:
            structured[budget] = _run_policy(
                protocol,
                branch_state,
                MoleculeBudgetPolicy(
                    budget.maximum_component_size,
                    budget.maximum_cycle_rank,
                ),
            )
            direction_runs.append((budget.branch_name, structured[budget]))
        full = _run_policy(protocol, branch_state, FullCollisionPolicy())
        direction_runs.append(("full", full))

        target = structured[protocol.selected_budget]
        accepted_by_layer, encounters_by_layer = _layer_counts(target.encounter_events)
        random_control = _run_policy(
            protocol,
            branch_state,
            QuotaMatchedRandomPolicy(
                target_accepted_by_layer=accepted_by_layer,
                target_encounters_by_layer=encounters_by_layer,
                seed=protocol.random_seed_offset + 1000 * particle_count + seed,
            ),
        )
        direction_runs.append(("count-time-matched-random", random_control))
        topology_name = f"topology-shuffled-{protocol.selected_budget.branch_name}"
        topology_control = _run_policy(
            protocol,
            branch_state,
            TopologyShuffledBudgetPolicy(
                maximum_component_size=protocol.selected_budget.maximum_component_size,
                maximum_cycle_rank=protocol.selected_budget.maximum_cycle_rank,
                seed=protocol.topology_seed_offset + 1000 * particle_count + seed,
            ),
        )
        direction_runs.append((topology_name, topology_control))

        full_count = len(full.accepted_encounters)
        for name, result in direction_runs:
            branches.append(E2BranchRun(direction, name, result))
            metrics.extend(
                _metric_rows(
                    protocol,
                    particle_count,
                    seed,
                    direction,
                    name,
                    result,
                    colors,
                    pivot_score,
                )
            )
            audits.append(
                _branch_audit(
                    particle_count,
                    seed,
                    direction,
                    name,
                    result,
                    full,
                    full_count,
                )
            )
    return E2CaseResult(
        particle_count=particle_count,
        seed=seed,
        initial_state=initial,
        colors=colors,
        preparation=preparation,
        pivot_score=pivot_score,
        branches=tuple(branches),
        metrics=tuple(metrics),
        audits=tuple(audits),
    )


def _prepare_case(
    protocol: MolecularEchoesE2Protocol,
    *,
    particle_count: int,
    seed: int,
) -> tuple[DiskState, PassiveColorMap, SimulationResult, DiskState]:
    initial, colors = prepare_echo_initial_state(
        protocol.e1_protocol,
        particle_count=particle_count,
        seed=seed,
    )
    preparation = HardDiskEDMD(protocol.e1_protocol.domain).run(
        initial,
        end_time=protocol.e1_protocol.preparation_time,
        sample_interval=protocol.e1_protocol.sample_interval,
    )
    return initial, colors, preparation, preparation.snapshots[-1].state


def _run_policy(
    protocol: MolecularEchoesE2Protocol,
    state: DiskState,
    policy: object,
) -> ModifiedSimulationResult:
    blocks_x, blocks_y = protocol.e1_protocol.chaotization_blocks

    def block_locator(position: tuple[float, float]) -> str:
        domain = protocol.e1_protocol.domain
        ix = min(blocks_x - 1, int((position[0] - domain.lower[0]) / domain.width * blocks_x))
        iy = min(blocks_y - 1, int((position[1] - domain.lower[1]) / domain.height * blocks_y))
        return f"{ix}:{iy}"

    return ModifiedHardDiskEDMD(
        protocol.e1_protocol.domain,
        policy,  # type: ignore[arg-type]
        layer_width=protocol.layer_width,
        block_locator=block_locator,
    ).run(
        state,
        end_time=protocol.e1_protocol.future_horizon,
        sample_interval=protocol.e1_protocol.sample_interval,
    )


def _metric_rows(
    protocol: MolecularEchoesE2Protocol,
    particle_count: int,
    seed: int,
    direction: E2Direction,
    branch: str,
    result: ModifiedSimulationResult,
    colors: PassiveColorMap,
    pivot_score: float,
) -> tuple[E2MetricRow, ...]:
    denominator = max(1.0 - pivot_score, 1.0e-15)
    return tuple(
        E2MetricRow(
            particle_count=particle_count,
            seed=seed,
            direction=direction,
            branch=branch,
            time=snapshot.time,
            color_score=(
                score := color_score(snapshot.state, colors, protocol.e1_protocol)
            ),
            color_recovery=(score - pivot_score) / denominator,
        )
        for snapshot in result.simulation.snapshots
    )


def _branch_audit(
    particle_count: int,
    seed: int,
    direction: E2Direction,
    branch: str,
    result: ModifiedSimulationResult,
    full: ModifiedSimulationResult,
    full_count: int,
) -> E2BranchAudit:
    accepted_by_layer, encounters_by_layer = _layer_counts(result.encounter_events)
    return E2BranchAudit(
        particle_count=particle_count,
        seed=seed,
        direction=direction,
        branch=branch,
        encounter_count=len(result.encounter_events),
        accepted_collision_count=len(result.accepted_encounters),
        suppressed_overlap_count=len(result.suppressed_encounters),
        collision_dose=len(result.accepted_encounters) / max(full_count, 1),
        incoming_pair_closure_defect=_incoming_pair_closure_defect(
            result.accepted_encounters
        ),
        mirrored_pair_alignment=_mirrored_pair_alignment(
            result.accepted_encounters,
            full.accepted_encounters,
        ),
        maximum_simultaneous_overlaps=result.maximum_simultaneous_overlaps,
        accepted_by_layer=tuple(sorted(accepted_by_layer.items())),
        encounters_by_layer=tuple(sorted(encounters_by_layer.items())),
    )


def _layer_counts(
    events: tuple[EncounterEvent, ...],
) -> tuple[dict[int, int], dict[int, int]]:
    encounters = Counter(event.layer for event in events)
    accepted = Counter(
        event.layer
        for event in events
        if event.decision is EncounterDecision.ACCEPT
    )
    return dict(accepted), dict(encounters)


def _incoming_pair_closure_defect(events: tuple[EncounterEvent, ...]) -> float:
    if len(events) < 2:
        return 0.0
    left = [
        event.pre_velocity_a[0] * event.contact_normal[0]
        + event.pre_velocity_a[1] * event.contact_normal[1]
        for event in events
    ]
    right = [
        event.pre_velocity_b[0] * event.contact_normal[0]
        + event.pre_velocity_b[1] * event.contact_normal[1]
        for event in events
    ]
    mean_left = mean(left)
    mean_right = mean(right)
    covariance = mean(
        (a - mean_left) * (b - mean_right)
        for a, b in zip(left, right, strict=True)
    )
    variance = 0.5 * (
        mean((value - mean_left) ** 2 for value in left)
        + mean((value - mean_right) ** 2 for value in right)
    )
    return abs(covariance) / max(variance, 1.0e-15)


def _mirrored_pair_alignment(
    events: tuple[EncounterEvent, ...],
    full_events: tuple[EncounterEvent, ...],
) -> float:
    if not events:
        return 0.0
    reference = Counter((event.layer, event.ordered_pair) for event in full_events)
    matched = 0
    for event in events:
        key = (event.layer, event.ordered_pair)
        if reference[key] > 0:
            reference[key] -= 1
            matched += 1
    return matched / len(events)
