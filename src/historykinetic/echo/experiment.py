from __future__ import annotations

import random
from math import sqrt

from historykinetic.echo.audit import (
    audit_resolved_state,
    audit_reversal,
    branch_metrics,
    color_score,
    invariant_mismatch,
)
from historykinetic.echo.models import (
    BranchRun,
    EchoCaseResult,
    EchoStudyResult,
    PassiveColorMap,
)
from historykinetic.echo.protocol import EchoBranchKind, EchoE1Protocol
from historykinetic.solvers import (
    DiskState,
    HardDiskDSMC,
    HardDiskEDMD,
    SimulationResult,
    Snapshot,
    SolverDiagnostics,
    make_initial_state,
)


def prepare_echo_initial_state(
    protocol: EchoE1Protocol,
    *,
    particle_count: int,
    seed: int,
) -> tuple[DiskState, PassiveColorMap]:
    size = protocol.size_for_count(particle_count)
    state = make_initial_state(
        protocol.domain,
        particle_count=particle_count,
        radius=0.5 * size.diameter,
        mass=protocol.particle_mass,
        temperature=protocol.temperature,
        mean_velocity=protocol.mean_velocity,
        seed=seed,
    )
    mean_x = sum(velocity[0] for velocity in state.velocities) / particle_count
    mean_y = sum(velocity[1] for velocity in state.velocities) / particle_count
    centered_x = [velocity[0] - mean_x for velocity in state.velocities]
    centered_y = [velocity[1] - mean_y for velocity in state.velocities]
    variance_x = (
        protocol.particle_mass * sum(value * value for value in centered_x) / particle_count
    )
    variance_y = (
        protocol.particle_mass * sum(value * value for value in centered_y) / particle_count
    )
    if variance_x <= 0 or variance_y <= 0:
        raise ValueError("anisotropic initialization requires nonzero component variance")
    scale_x = sqrt(protocol.temperature_x / variance_x)
    scale_y = sqrt(protocol.temperature_y / variance_y)
    state.velocities = [
        (
            protocol.mean_velocity[0] + scale_x * vx,
            protocol.mean_velocity[1] + scale_y * vy,
        )
        for vx, vy in zip(centered_x, centered_y, strict=True)
    ]
    labels = [0] * particle_count
    for particle_id, position in zip(state.particle_ids, state.positions, strict=True):
        labels[particle_id] = int(protocol.pattern.contains(position))
    return state, PassiveColorMap(tuple(labels))


def reverse_state(state: DiskState) -> DiskState:
    reversed_state = state.copy()
    reversed_state.velocities = [
        (-velocity[0], -velocity[1]) for velocity in reversed_state.velocities
    ]
    return reversed_state


def chaotize_velocities(
    state: DiskState,
    colors: PassiveColorMap,
    protocol: EchoE1Protocol,
    *,
    seed: int,
) -> tuple[DiskState, float]:
    candidate = state.copy()
    blocks_x, blocks_y = protocol.chaotization_blocks
    groups: dict[tuple[int, int, int], list[int]] = {}
    for index, (position, particle_id) in enumerate(
        zip(candidate.positions, candidate.particle_ids, strict=True)
    ):
        normalized_x = (position[0] - protocol.domain.lower[0]) / protocol.domain.width
        normalized_y = (position[1] - protocol.domain.lower[1]) / protocol.domain.height
        ix = min(blocks_x - 1, max(0, int(normalized_x * blocks_x)))
        iy = min(blocks_y - 1, max(0, int(normalized_y * blocks_y)))
        groups.setdefault((ix, iy, colors.label(particle_id)), []).append(index)

    rng = random.Random(protocol.chaotization_seed_offset + seed)
    changed = 0
    for key in sorted(groups):
        members = sorted(groups[key], key=lambda index: candidate.particle_ids[index])
        if len(members) <= 1:
            continue
        source_velocities = [candidate.velocities[index] for index in members]
        permutation = list(range(len(members)))
        _sattolo_cycle(permutation, rng)
        for destination, source in enumerate(permutation):
            index = members[destination]
            replacement = source_velocities[source]
            changed += int(candidate.velocities[index] != replacement)
            candidate.velocities[index] = replacement
    return candidate, changed / candidate.particle_count


def construct_echo_branches(
    pivot: DiskState,
    colors: PassiveColorMap,
    protocol: EchoE1Protocol,
    *,
    seed: int,
) -> tuple[DiskState, DiskState, DiskState, float]:
    exact_reverse = reverse_state(pivot)
    chaotized_reverse, changed_fraction = chaotize_velocities(
        exact_reverse,
        colors,
        protocol,
        seed=seed,
    )
    return pivot.copy(), exact_reverse, chaotized_reverse, changed_fraction


def run_echo_e1(protocol: EchoE1Protocol) -> EchoStudyResult:
    cases: list[EchoCaseResult] = []
    for size in protocol.sizes:
        for seed in protocol.seeds:
            cases.append(
                _run_echo_case(
                    protocol,
                    particle_count=size.count,
                    seed=seed,
                )
            )
    return EchoStudyResult(protocol=protocol, cases=tuple(cases))


def _run_echo_case(
    protocol: EchoE1Protocol,
    *,
    particle_count: int,
    seed: int,
) -> EchoCaseResult:
    initial_state, colors = prepare_echo_initial_state(
        protocol,
        particle_count=particle_count,
        seed=seed,
    )
    preparation = HardDiskEDMD(protocol.domain).run(
        initial_state,
        end_time=protocol.preparation_time,
        sample_interval=protocol.sample_interval,
    )
    pivot = preparation.snapshots[-1].state
    forward_state, exact_reverse_state, chaotized_state, changed_fraction = (
        construct_echo_branches(pivot, colors, protocol, seed=seed)
    )
    forward = HardDiskEDMD(protocol.domain).run(
        forward_state,
        end_time=protocol.future_horizon,
        sample_interval=protocol.sample_interval,
    )
    exact_reverse = HardDiskEDMD(protocol.domain).run(
        exact_reverse_state,
        end_time=protocol.future_horizon,
        sample_interval=protocol.sample_interval,
    )
    chaotized_reverse = HardDiskEDMD(protocol.domain).run(
        chaotized_state,
        end_time=protocol.future_horizon,
        sample_interval=protocol.sample_interval,
    )
    dsmc_reverse = HardDiskDSMC(
        protocol.domain,
        cells_x=protocol.dsmc_cells[0],
        cells_y=protocol.dsmc_cells[1],
        time_step=protocol.dsmc_time_step,
        seed=protocol.dsmc_seed_offset + seed,
    ).run(
        exact_reverse_state,
        end_time=protocol.future_horizon,
        sample_interval=protocol.sample_interval,
    )
    ghost = _run_ghost(
        exact_reverse_state,
        protocol,
    )
    branches = (
        BranchRun(EchoBranchKind.FORWARD, forward),
        BranchRun(EchoBranchKind.EXACT_REVERSE, exact_reverse),
        BranchRun(EchoBranchKind.CHAOTIZED_REVERSE, chaotized_reverse),
        BranchRun(EchoBranchKind.DSMC_REVERSE, dsmc_reverse),
        BranchRun(EchoBranchKind.GHOST, ghost),
    )
    reversal_audit = audit_reversal(
        particle_count=particle_count,
        seed=seed,
        initial_state=initial_state,
        forward=preparation,
        reverse=exact_reverse,
        protocol=protocol,
    )
    resolved_audits = tuple(
        audit_resolved_state(
            particle_count=particle_count,
            seed=seed,
            reference=exact_reverse_state,
            candidate=chaotized_state,
            colors=colors,
            protocol=protocol,
            spatial_grid=grid,
            velocity_edges_standardized=velocity_edges,
        )
        for grid in protocol.audit_spatial_grids
        for velocity_edges in protocol.audit_velocity_edges_standardized
    )
    pivot_score = color_score(exact_reverse_state, colors, protocol)
    metrics = tuple(
        metric
        for branch in branches
        for metric in branch_metrics(
            particle_count=particle_count,
            seed=seed,
            kind=branch.kind,
            result=branch.result,
            colors=colors,
            protocol=protocol,
            pivot_score=pivot_score,
        )
    )
    return EchoCaseResult(
        particle_count=particle_count,
        seed=seed,
        initial_state=initial_state,
        colors=colors,
        preparation=preparation,
        pivot_reverse_state=exact_reverse_state,
        branches=branches,
        reversal_audit=reversal_audit,
        resolved_state_audits=resolved_audits,
        changed_particle_fraction=changed_fraction,
        invariant_mismatch=invariant_mismatch(exact_reverse_state, chaotized_state),
        metrics=metrics,
    )


def _run_ghost(
    initial_state: DiskState,
    protocol: EchoE1Protocol,
) -> SimulationResult:
    sample_times = _sample_times(protocol.future_horizon, protocol.sample_interval)
    snapshots: list[Snapshot] = []
    for time in sample_times:
        state = initial_state.copy()
        state.positions = [
            protocol.domain.wrap(
                (
                    position[0] + velocity[0] * time,
                    position[1] + velocity[1] * time,
                )
            )
            for position, velocity in zip(
                initial_state.positions, initial_state.velocities, strict=True
            )
        ]
        snapshots.append(Snapshot(time=time, state=state))
    diagnostics = SolverDiagnostics(
        initial_mass=initial_state.total_mass,
        final_mass=initial_state.total_mass,
        initial_energy=initial_state.kinetic_energy,
        final_energy=initial_state.kinetic_energy,
        initial_momentum=initial_state.momentum,
        final_momentum=initial_state.momentum,
        particle_collision_count=0,
        boundary_collision_count=0,
    )
    return SimulationResult(
        backend="ballistic_ghost_reference",
        event_semantics="geometric_collision",
        snapshots=tuple(snapshots),
        collision_events=(),
        diagnostics=diagnostics,
    )


def _sample_times(end_time: float, interval: float) -> tuple[float, ...]:
    count = int(end_time / interval + 1.0e-12)
    times = [index * interval for index in range(count + 1)]
    if end_time - times[-1] > 1.0e-12:
        times.append(end_time)
    else:
        times[-1] = end_time
    return tuple(times)


def _sattolo_cycle(values: list[int], rng: random.Random) -> None:
    for index in range(len(values) - 1, 0, -1):
        replacement = rng.randrange(index)
        values[index], values[replacement] = values[replacement], values[index]
