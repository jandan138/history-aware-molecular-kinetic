"""Exact conservative branching over an addressable collision timeline."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, replace
from math import ceil, inf, sqrt
from time import perf_counter
from typing import Literal

from historykinetic.contracts import CollisionEvent
from historykinetic.solvers import (
    BoundaryKind,
    DiskState,
    Domain2D,
    HardDiskEDMD,
    SimulationResult,
    Snapshot,
    SolverDiagnostics,
    validate_state_geometry,
)
from historykinetic.solvers.hard_disk_physics import (
    TIME_EPS,
    advance_state,
    predict_pair_collision,
    resolve_pair_collision,
)
from historykinetic.solvers.state import minimum_image

from .edit import (
    EditAudit,
    PairRelativeVelocityRotationEdit,
    apply_pair_relative_velocity_rotation,
)
from .models import CausalCheckpoint, TimelineRun


@dataclass(frozen=True, slots=True)
class BranchCollisionEvent:
    event_id: str
    ordinal: int
    event: CollisionEvent
    source: Literal["reused_baseline", "recomputed"]
    baseline_event_id: str | None
    affected_particle_count: int


@dataclass(frozen=True, slots=True)
class CausalBranchDiagnostics:
    postfork_baseline_event_count: int
    reused_baseline_event_count: int
    invalidated_baseline_event_count: int
    recomputed_event_count: int
    stale_candidate_event_count: int
    peak_affected_particle_count: int
    terminal_affected_particle_count: int
    particle_count: int

    @property
    def baseline_event_reuse_fraction(self) -> float:
        return self.reused_baseline_event_count / max(self.postfork_baseline_event_count, 1)

    @property
    def peak_affected_fraction(self) -> float:
        return self.peak_affected_particle_count / self.particle_count


@dataclass(frozen=True, slots=True)
class CausalBranchRun:
    checkpoint: CausalCheckpoint
    edit: PairRelativeVelocityRotationEdit
    edit_audit: EditAudit
    simulation: SimulationResult
    events: tuple[BranchCollisionEvent, ...]
    affected_particle_ids: tuple[int, ...]
    affected_history: tuple[tuple[float, tuple[int, ...]], ...]
    diagnostics: CausalBranchDiagnostics


@dataclass(frozen=True, slots=True)
class BranchComparison:
    local_event_count: int
    full_event_count: int
    collision_pair_agreement: float
    maximum_collision_time_error: float
    terminal_position_rms: float
    terminal_velocity_rms: float


@dataclass(frozen=True, slots=True)
class BranchTiming:
    """Reference wall times, recorded for transparency rather than a speed claim."""

    local_seconds: float
    full_resimulation_seconds: float


@dataclass(frozen=True, slots=True)
class CausalBranchPreview:
    """One exact local branch intended for a responsive authoring preview.

    A preview uses the same conservative causal scheduler as a verified branch,
    but deliberately does not launch the complete full-resimulation oracle.  A
    caller that wants to publish or save a chosen branch must still call
    :func:`fork_causal_branch`, which performs that one final comparison.
    """

    local: CausalBranchRun
    local_seconds: float


@dataclass(frozen=True, slots=True)
class CausalBranchResult:
    local: CausalBranchRun
    full_resimulation: SimulationResult
    comparison: BranchComparison
    timing: BranchTiming


@dataclass(frozen=True, slots=True)
class _CandidateEvent:
    time: float
    sequence: int
    left: int
    right: int
    count_left: int
    count_right: int
    normal: tuple[float, float]

    def heap_key(self) -> tuple[float, int, _CandidateEvent]:
        return (self.time, self.sequence, self)


def fork_causal_branch(
    timeline: TimelineRun,
    domain: Domain2D,
    *,
    checkpoint: CausalCheckpoint,
    edit: PairRelativeVelocityRotationEdit,
    end_time: float,
    sample_interval: float,
) -> CausalBranchResult:
    """Edit a checkpoint and exactly recompute only its growing causal cone.

    The first implementation intentionally supports the paper's periodic hero
    scene.  There are no hidden wall events in that scene: every physical event
    is therefore an addressable particle-pair collision.
    """

    preview = preview_causal_branch(
        timeline,
        domain,
        checkpoint=checkpoint,
        edit=edit,
        end_time=end_time,
        sample_interval=sample_interval,
    )
    edited_state, _ = apply_pair_relative_velocity_rotation(checkpoint.state, edit)
    full_start = perf_counter()
    full = _run_full_resimulation(
        edited_state,
        domain,
        start_time=checkpoint.time,
        end_time=end_time,
    )
    full_seconds = perf_counter() - full_start
    return CausalBranchResult(
        local=preview.local,
        full_resimulation=full,
        comparison=_compare_branch_runs(preview.local.simulation, full, domain),
        timing=BranchTiming(
            local_seconds=preview.local_seconds,
            full_resimulation_seconds=full_seconds,
        ),
    )


def preview_causal_branch(
    timeline: TimelineRun,
    domain: Domain2D,
    *,
    checkpoint: CausalCheckpoint,
    edit: PairRelativeVelocityRotationEdit,
    end_time: float,
    sample_interval: float,
) -> CausalBranchPreview:
    """Run one exact causal preview without a full-resimulation oracle.

    This separates the creator-facing loop from the publishing check.  The
    preview is still physical: it applies the same conservative edit and exact
    local causal recomputation as :func:`fork_causal_branch`; it simply avoids
    spending an additional global run on every angle the creator briefly views.
    """

    _validate_branch_request(domain, checkpoint, end_time, sample_interval)
    edited_state, edit_audit = apply_pair_relative_velocity_rotation(checkpoint.state, edit)
    local_start = perf_counter()
    local = _run_local_branch(
        timeline,
        domain,
        checkpoint=checkpoint,
        edited_state=edited_state,
        edit=edit,
        edit_audit=edit_audit,
        end_time=end_time,
        sample_interval=sample_interval,
    )
    return CausalBranchPreview(
        local=local,
        local_seconds=perf_counter() - local_start,
    )


def _validate_branch_request(
    domain: Domain2D,
    checkpoint: CausalCheckpoint,
    end_time: float,
    sample_interval: float,
) -> None:
    if domain.boundary is not BoundaryKind.PERIODIC:
        raise ValueError("causal branching v0 supports periodic domains")
    if checkpoint.time >= end_time:
        raise ValueError("branch end_time must be later than its checkpoint")
    if sample_interval <= 0:
        raise ValueError("sample_interval must be positive")


def _run_local_branch(
    timeline: TimelineRun,
    domain: Domain2D,
    *,
    checkpoint: CausalCheckpoint,
    edited_state: DiskState,
    edit: PairRelativeVelocityRotationEdit,
    edit_audit: EditAudit,
    end_time: float,
    sample_interval: float,
) -> CausalBranchRun:
    state = edited_state.copy()
    initial_mass = state.total_mass
    initial_energy = state.kinetic_energy
    initial_momentum = state.momentum
    index_by_id = {particle_id: index for index, particle_id in enumerate(state.particle_ids)}
    affected = {index_by_id[particle_id] for particle_id in edit.pair}
    counts = [0] * state.particle_count
    candidate_heap: list[tuple[float, int, _CandidateEvent]] = []
    candidate_sequence = 0
    current_time = checkpoint.time
    stale_candidates = 0

    def schedule_pairs(changed: set[int]) -> None:
        nonlocal candidate_sequence
        pairs: set[tuple[int, int]] = set()
        for particle in changed:
            for other in range(state.particle_count):
                if particle == other:
                    continue
                left, right = sorted((particle, other))
                if left not in affected and right not in affected:
                    continue
                pairs.add((left, right))
        for left, right in sorted(pairs):
            prediction = predict_pair_collision(
                state,
                domain,
                left,
                right,
                end_time - current_time,
            )
            if prediction is None:
                continue
            dt, normal = prediction
            event = _CandidateEvent(
                time=current_time + dt,
                sequence=candidate_sequence,
                left=left,
                right=right,
                count_left=counts[left],
                count_right=counts[right],
                normal=normal,
            )
            candidate_sequence += 1
            heapq.heappush(candidate_heap, event.heap_key())

    def peek_candidate() -> _CandidateEvent | None:
        nonlocal stale_candidates
        while candidate_heap:
            event = candidate_heap[0][2]
            if event.count_left != counts[event.left] or event.count_right != counts[event.right]:
                heapq.heappop(candidate_heap)
                stale_candidates += 1
                continue
            return event
        return None

    schedule_pairs(set(affected))
    baseline_events = tuple(
        event
        for event in timeline.events
        if event.time > checkpoint.time + TIME_EPS and event.time <= end_time + TIME_EPS
    )
    baseline_index = 0
    reused_count = 0
    invalidated_count = 0
    recomputed_count = 0
    branch_events: list[BranchCollisionEvent] = []
    affected_history: list[tuple[float, tuple[int, ...]]] = [
        (checkpoint.time, _affected_ids(state, affected))
    ]
    peak_affected_count = len(affected)
    sample_times = _registered_sample_times(checkpoint.time, end_time, sample_interval)
    snapshots = [Snapshot(checkpoint.time, state.copy())]
    sample_index = 1

    while sample_index < len(sample_times):
        sample_time = sample_times[sample_index]
        baseline = (
            baseline_events[baseline_index] if baseline_index < len(baseline_events) else None
        )
        candidate = peek_candidate()
        baseline_time = baseline.time if baseline is not None else inf
        candidate_time = candidate.time if candidate is not None else inf
        next_event_time = min(baseline_time, candidate_time)
        if next_event_time > sample_time + TIME_EPS:
            advance_state(state, domain, sample_time - current_time)
            current_time = sample_time
            snapshots.append(Snapshot(sample_time, state.copy()))
            sample_index += 1
            continue

        use_candidate = candidate is not None and candidate_time <= baseline_time
        if use_candidate:
            assert candidate is not None
            heapq.heappop(candidate_heap)
            advance_state(state, domain, max(0.0, candidate.time - current_time))
            current_time = candidate.time
            collision = resolve_pair_collision(
                state,
                domain,
                left=candidate.left,
                right=candidate.right,
                normal=candidate.normal,
                time=current_time,
            )
            previously_affected = len(affected)
            affected.update((candidate.left, candidate.right))
            if len(affected) != previously_affected:
                affected_history.append((current_time, _affected_ids(state, affected)))
            peak_affected_count = max(peak_affected_count, len(affected))
            counts[candidate.left] += 1
            counts[candidate.right] += 1
            schedule_pairs({candidate.left, candidate.right})
            branch_events.append(
                BranchCollisionEvent(
                    event_id=f"branch-collision-{len(branch_events):06d}",
                    ordinal=len(branch_events),
                    event=collision,
                    source="recomputed",
                    baseline_event_id=None,
                    affected_particle_count=len(affected),
                )
            )
            recomputed_count += 1
            continue

        assert baseline is not None
        baseline_index += 1
        advance_state(state, domain, max(0.0, baseline.time - current_time))
        current_time = baseline.time
        left = index_by_id[baseline.particle_a]
        right = index_by_id[baseline.particle_b]
        if left in affected or right in affected:
            promoted = {left, right} - affected
            if promoted:
                affected.update(promoted)
                affected_history.append((current_time, _affected_ids(state, affected)))
                peak_affected_count = max(peak_affected_count, len(affected))
                schedule_pairs(promoted)
            invalidated_count += 1
            continue

        collision = resolve_pair_collision(
            state,
            domain,
            left=left,
            right=right,
            normal=baseline.contact_normal,
            time=current_time,
        )
        counts[left] += 1
        counts[right] += 1
        schedule_pairs({left, right})
        branch_events.append(
            BranchCollisionEvent(
                event_id=f"branch-collision-{len(branch_events):06d}",
                ordinal=len(branch_events),
                event=collision,
                source="reused_baseline",
                baseline_event_id=baseline.event_id,
                affected_particle_count=len(affected),
            )
        )
        reused_count += 1

    validate_state_geometry(state, domain, overlap_tolerance=5.0e-9)
    diagnostics = SolverDiagnostics(
        initial_mass=initial_mass,
        final_mass=state.total_mass,
        initial_energy=initial_energy,
        final_energy=state.kinetic_energy,
        initial_momentum=initial_momentum,
        final_momentum=state.momentum,
        particle_collision_count=len(branch_events),
        boundary_collision_count=0,
        stale_event_count=stale_candidates,
    )
    simulation = SimulationResult(
        backend="python_causal_branch_reference",
        event_semantics="geometric_collision",
        snapshots=tuple(snapshots),
        collision_events=tuple(item.event for item in branch_events),
        diagnostics=diagnostics,
    )
    return CausalBranchRun(
        checkpoint=checkpoint,
        edit=edit,
        edit_audit=edit_audit,
        simulation=simulation,
        events=tuple(branch_events),
        affected_particle_ids=_affected_ids(state, affected),
        affected_history=tuple(affected_history),
        diagnostics=CausalBranchDiagnostics(
            postfork_baseline_event_count=len(baseline_events),
            reused_baseline_event_count=reused_count,
            invalidated_baseline_event_count=invalidated_count,
            recomputed_event_count=recomputed_count,
            stale_candidate_event_count=stale_candidates,
            peak_affected_particle_count=peak_affected_count,
            terminal_affected_particle_count=len(affected),
            particle_count=state.particle_count,
        ),
    )


def _run_full_resimulation(
    edited_state: DiskState,
    domain: Domain2D,
    *,
    start_time: float,
    end_time: float,
) -> SimulationResult:
    duration = end_time - start_time
    raw = HardDiskEDMD(domain).run(
        edited_state,
        end_time=duration,
        sample_interval=duration,
    )
    return SimulationResult(
        backend="python_edmd_full_branch_oracle",
        event_semantics=raw.event_semantics,
        snapshots=tuple(
            Snapshot(time=start_time + snapshot.time, state=snapshot.state)
            for snapshot in raw.snapshots
        ),
        collision_events=tuple(
            replace(event, time=start_time + event.time) for event in raw.collision_events
        ),
        diagnostics=raw.diagnostics,
        geometry_collision_events=raw.geometry_collision_events,
    )


def _compare_branch_runs(
    local: SimulationResult,
    full: SimulationResult,
    domain: Domain2D,
) -> BranchComparison:
    common = min(len(local.collision_events), len(full.collision_events))
    matching_pairs = sum(
        local.collision_events[index].ordered_pair == full.collision_events[index].ordered_pair
        for index in range(common)
    )
    denominator = max(len(local.collision_events), len(full.collision_events), 1)
    time_errors = [
        abs(local.collision_events[index].time - full.collision_events[index].time)
        for index in range(common)
    ]
    local_terminal = local.snapshots[-1].state
    full_terminal = full.snapshots[-1].state
    position_error = 0.0
    velocity_error = 0.0
    for local_position, full_position, local_velocity, full_velocity in zip(
        local_terminal.positions,
        full_terminal.positions,
        local_terminal.velocities,
        full_terminal.velocities,
        strict=True,
    ):
        displacement = minimum_image(
            (
                local_position[0] - full_position[0],
                local_position[1] - full_position[1],
            ),
            domain,
        )
        position_error += displacement[0] ** 2 + displacement[1] ** 2
        velocity_error += (local_velocity[0] - full_velocity[0]) ** 2 + (
            local_velocity[1] - full_velocity[1]
        ) ** 2
    count = local_terminal.particle_count
    return BranchComparison(
        local_event_count=len(local.collision_events),
        full_event_count=len(full.collision_events),
        collision_pair_agreement=matching_pairs / denominator,
        maximum_collision_time_error=max(time_errors, default=0.0),
        terminal_position_rms=sqrt(position_error / count),
        terminal_velocity_rms=sqrt(velocity_error / count),
    )


def _registered_sample_times(start: float, end: float, interval: float) -> tuple[float, ...]:
    first_index = ceil((start + TIME_EPS) / interval)
    times = [start]
    index = first_index
    while index * interval < end - TIME_EPS:
        times.append(index * interval)
        index += 1
    times.append(end)
    return tuple(times)


def _affected_ids(state: DiskState, affected: set[int]) -> tuple[int, ...]:
    return tuple(sorted(state.particle_ids[index] for index in affected))
