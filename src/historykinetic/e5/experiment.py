"""Run the registered E5 Same Present, Chosen Future authoring session."""

from __future__ import annotations

from math import sqrt
from statistics import median
from time import perf_counter

from historykinetic.echo import prepare_echo_initial_state, reverse_state
from historykinetic.echo.models import PassiveColorMap
from historykinetic.solvers import DiskState, Domain2D, HardDiskEDMD, SimulationResult
from historykinetic.solvers.state import minimum_image

from .models import (
    E5Metrics,
    FutureOutcomeMetrics,
    FutureTarget,
    MolecularTimeMachineE5Result,
    PivotReplayAudit,
    SurgeryPreview,
)
from .protocol import MolecularTimeMachineE5Protocol
from .surgery import apply_velocity_ownership_surgery, enumerate_target_surgeries


def run_molecular_time_machine_e5(
    protocol: MolecularTimeMachineE5Protocol,
) -> MolecularTimeMachineE5Result:
    """Choose a terminal stroke, preserve the present, and author a new future."""

    e1 = protocol.e1_protocol
    initial_state, colors = prepare_echo_initial_state(
        e1,
        particle_count=protocol.hero.particle_count,
        seed=protocol.hero.seed,
    )
    preparation = HardDiskEDMD(e1.domain).run(
        initial_state,
        end_time=e1.preparation_time,
        sample_interval=protocol.sample_interval,
    )
    baseline = HardDiskEDMD(e1.domain).run(
        reverse_state(preparation.snapshots[-1].state),
        end_time=protocol.end_time,
        sample_interval=protocol.sample_interval,
    )
    target = _resolve_target(protocol, baseline, colors)
    pivot_state = _state_at_registered_time(protocol, baseline)
    remaining_time = protocol.end_time - protocol.hero.pivot_time
    pivot_replay = HardDiskEDMD(e1.domain).run(
        pivot_state,
        end_time=remaining_time,
        sample_interval=protocol.sample_interval,
    )
    replay_audit = _audit_pivot_replay(baseline, pivot_replay, e1.domain)

    surgeries = enumerate_target_surgeries(
        pivot_state,
        e1.domain,
        pivot_time=protocol.hero.pivot_time,
        target_particle_ids=target.particle_ids,
        declared_spatial_grid=protocol.surgery.declared_spatial_grid,
        maximum_disjoint_swaps=protocol.surgery.maximum_disjoint_swaps,
    )
    if len(surgeries) != protocol.hero.expected_preview_count:
        raise RuntimeError(
            "frozen E5 candidate palette drifted: "
            f"expected {protocol.hero.expected_preview_count}, got {len(surgeries)}"
        )

    previews: list[SurgeryPreview] = []
    for surgery in surgeries:
        edited_pivot, audit = apply_velocity_ownership_surgery(
            pivot_state,
            e1.domain,
            surgery,
            target_particle_ids=target.particle_ids,
        )
        started = perf_counter()
        simulation = HardDiskEDMD(e1.domain).run(
            edited_pivot,
            end_time=remaining_time,
            sample_interval=protocol.sample_interval,
        )
        wall_seconds = perf_counter() - started
        previews.append(
            SurgeryPreview(
                surgery=surgery,
                edited_pivot=edited_pivot,
                audit=audit,
                simulation=simulation,
                outcome=_measure_outcome(protocol, baseline, simulation, colors, target),
                wall_seconds=wall_seconds,
            )
        )

    selected = _select_preview(protocol, tuple(previews))
    if selected.surgery.swaps != protocol.hero.expected_selected_swaps:
        raise RuntimeError(
            "frozen E5 selected surgery drifted: "
            f"expected {protocol.hero.expected_selected_swaps}, got {selected.surgery.swaps}"
        )
    metrics = E5Metrics(
        preview_count=len(previews),
        preview_median_seconds=median(preview.wall_seconds for preview in previews),
        selected_swap_count=len(selected.surgery.swaps),
        touched_particle_count=len(selected.surgery.touched_particle_ids),
        touched_particle_fraction=(
            len(selected.surgery.touched_particle_ids) / protocol.hero.particle_count
        ),
        target_ejection_fraction=selected.outcome.target_ejection_fraction,
        target_region_reduction_fraction=selected.outcome.target_region_reduction_fraction,
        collateral_retention_fraction=selected.outcome.collateral_retention_fraction,
    )
    return MolecularTimeMachineE5Result(
        protocol=protocol,
        colors=colors,
        preparation=preparation,
        baseline=baseline,
        pivot_state=pivot_state,
        pivot_replay=pivot_replay,
        pivot_replay_audit=replay_audit,
        target=target,
        previews=tuple(previews),
        selected_preview=selected,
        metrics=metrics,
    )


def _resolve_target(
    protocol: MolecularTimeMachineE5Protocol,
    baseline: SimulationResult,
    colors: PassiveColorMap,
) -> FutureTarget:
    terminal = baseline.snapshots[-1].state
    target_ids = tuple(
        particle_id
        for particle_id, position in zip(terminal.particle_ids, terminal.positions, strict=True)
        if colors.label(particle_id) == 1 and _inside_target(protocol, position)
    )
    expected = protocol.hero.target.expected_foreground_particle_ids
    if target_ids != expected:
        raise RuntimeError(
            f"frozen E5 target membership drifted: expected {expected}, got {target_ids}"
        )
    target_set = set(target_ids)
    collateral = tuple(
        particle_id
        for particle_id, position in zip(terminal.particle_ids, terminal.positions, strict=True)
        if colors.label(particle_id) == 1
        and protocol.e1_protocol.pattern.contains(position)
        and particle_id not in target_set
    )
    return FutureTarget(
        target_id=protocol.hero.target.target_id,
        description=protocol.hero.target.description,
        x_bounds=protocol.hero.target.x_bounds,
        y_bounds=protocol.hero.target.y_bounds,
        particle_ids=target_ids,
        collateral_foreground_particle_ids=collateral,
    )


def _state_at_registered_time(
    protocol: MolecularTimeMachineE5Protocol,
    baseline: SimulationResult,
) -> DiskState:
    pivot = min(
        baseline.snapshots,
        key=lambda snapshot: abs(snapshot.time - protocol.hero.pivot_time),
    )
    if abs(pivot.time - protocol.hero.pivot_time) > protocol.hero.recipe_tolerance:
        raise RuntimeError("E5 baseline does not contain the registered pivot time")
    return pivot.state.copy()


def _measure_outcome(
    protocol: MolecularTimeMachineE5Protocol,
    baseline: SimulationResult,
    edited: SimulationResult,
    colors: PassiveColorMap,
    target: FutureTarget,
) -> FutureOutcomeMetrics:
    baseline_terminal = baseline.snapshots[-1].state
    edited_terminal = edited.snapshots[-1].state
    baseline_target_occupants = {
        particle_id
        for particle_id, position in zip(
            baseline_terminal.particle_ids, baseline_terminal.positions, strict=True
        )
        if colors.label(particle_id) == 1 and _inside_target(protocol, position)
    }
    edited_target_occupants = {
        particle_id
        for particle_id, position in zip(
            edited_terminal.particle_ids, edited_terminal.positions, strict=True
        )
        if colors.label(particle_id) == 1 and _inside_target(protocol, position)
    }
    target_set = set(target.particle_ids)
    target_ejected = tuple(sorted(target_set - edited_target_occupants))
    collateral_set = set(target.collateral_foreground_particle_ids)
    edited_inside_pattern = {
        particle_id
        for particle_id, position in zip(
            edited_terminal.particle_ids, edited_terminal.positions, strict=True
        )
        if colors.label(particle_id) == 1
        and protocol.e1_protocol.pattern.contains(position)
    }
    collateral_retained = tuple(sorted(collateral_set & edited_inside_pattern))
    baseline_occupancy = len(baseline_target_occupants)
    edited_occupancy = len(edited_target_occupants)
    return FutureOutcomeMetrics(
        target_particle_count=len(target_set),
        baseline_target_region_occupancy=baseline_occupancy,
        edited_target_region_occupancy=edited_occupancy,
        target_ejected_particle_ids=target_ejected,
        target_ejection_fraction=len(target_ejected) / max(len(target_set), 1),
        target_region_reduction_fraction=(
            (baseline_occupancy - edited_occupancy) / max(baseline_occupancy, 1)
        ),
        collateral_particle_count=len(collateral_set),
        collateral_retained_particle_ids=collateral_retained,
        collateral_retention_fraction=(
            len(collateral_retained) / max(len(collateral_set), 1)
        ),
        edited_foreground_inside_pattern_count=len(edited_inside_pattern),
    )


def _select_preview(
    protocol: MolecularTimeMachineE5Protocol,
    previews: tuple[SurgeryPreview, ...],
) -> SurgeryPreview:
    eligible = [
        preview
        for preview in previews
        if preview.outcome.collateral_retention_fraction
        >= protocol.acceptance.minimum_collateral_retention_fraction
    ]
    if not eligible:
        raise RuntimeError("E5 palette contains no surgery that preserves the non-target glyph")
    return min(
        eligible,
        key=lambda preview: (
            -preview.outcome.target_ejection_fraction,
            -preview.outcome.collateral_retention_fraction,
            len(preview.surgery.touched_particle_ids),
            preview.surgery.swaps,
        ),
    )


def _audit_pivot_replay(
    baseline: SimulationResult,
    replay: SimulationResult,
    domain: Domain2D,
) -> PivotReplayAudit:
    left = baseline.snapshots[-1].state
    right = replay.snapshots[-1].state
    squared_position = 0.0
    squared_velocity = 0.0
    for left_position, right_position, left_velocity, right_velocity in zip(
        left.positions,
        right.positions,
        left.velocities,
        right.velocities,
        strict=True,
    ):
        displacement = minimum_image(
            (
                right_position[0] - left_position[0],
                right_position[1] - left_position[1],
            ),
            domain,
        )
        squared_position += displacement[0] ** 2 + displacement[1] ** 2
        squared_velocity += (
            (right_velocity[0] - left_velocity[0]) ** 2
            + (right_velocity[1] - left_velocity[1]) ** 2
        )
    common = min(len(baseline.collision_events), len(replay.collision_events))
    baseline_tail = baseline.collision_events[-common:] if common else ()
    matching = sum(
        left_event.ordered_pair == right_event.ordered_pair
        for left_event, right_event in zip(
            baseline_tail, replay.collision_events, strict=True
        )
    )
    denominator = max(len(baseline_tail), len(replay.collision_events), 1)
    return PivotReplayAudit(
        terminal_position_rms=sqrt(squared_position / left.particle_count),
        terminal_velocity_rms=sqrt(squared_velocity / left.particle_count),
        collision_pair_agreement=matching / denominator,
    )


def _inside_target(
    protocol: MolecularTimeMachineE5Protocol,
    position: tuple[float, float],
) -> bool:
    x, y = position
    x0, x1 = protocol.hero.target.x_bounds
    y0, y1 = protocol.hero.target.y_bounds
    x_inside = x0 <= x <= x1 if protocol.hero.target.x_lower_inclusive else x0 < x <= x1
    return x_inside and y0 <= y <= y1
