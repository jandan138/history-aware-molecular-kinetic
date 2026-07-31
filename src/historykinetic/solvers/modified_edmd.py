"""Event-driven hard-disk dynamics with policy-suppressed overlaps.

This is the executable E2 analogue of the modified dynamics in which an
inadmissible geometric encounter is allowed to pass through without impulse.
The overlap is kept as explicit solver state until its geometrical exit, so a
velocity change caused by a third particle invalidates and recomputes that exit.
"""

from __future__ import annotations

import heapq
from collections.abc import Callable
from dataclasses import dataclass
from math import ceil, floor, hypot, sqrt

from historykinetic.contracts import CollisionEvent
from historykinetic.molecules.models import (
    EncounterContext,
    EncounterDecision,
    EncounterEvent,
    ModifiedSimulationResult,
    OverlapExitEvent,
)
from historykinetic.molecules.policies import CollisionPolicy
from historykinetic.molecules.tracker import MoleculeTracker
from historykinetic.solvers.result import SimulationResult, SolverDiagnostics
from historykinetic.solvers.state import (
    BoundaryKind,
    DiskState,
    Domain2D,
    Snapshot,
    validate_state_geometry,
)

_TIME_EPS = 1.0e-12
_CONTACT_EPS = 1.0e-10


@dataclass(frozen=True, slots=True)
class _ScheduledEvent:
    time: float
    sequence: int
    kind: str
    particle_a: int
    particle_b: int
    count_a: int
    count_b: int
    normal_x: float
    normal_y: float

    def heap_key(self) -> tuple[float, int, _ScheduledEvent]:
        return (self.time, self.sequence, self)


class ModifiedHardDiskEDMD:
    """Periodic EDMD whose encounter impulse is selected by a collision policy."""

    semantic_version = "0.1.0"
    name = "python_modified_edmd"

    def __init__(
        self,
        domain: Domain2D,
        policy: CollisionPolicy,
        *,
        layer_width: float,
        block_locator: Callable[[tuple[float, float]], str] | None = None,
    ) -> None:
        if domain.boundary is not BoundaryKind.PERIODIC or domain.obstacles:
            raise ValueError("modified E2 dynamics currently requires an empty periodic domain")
        if layer_width <= 0:
            raise ValueError("layer_width must be positive")
        self.domain = domain
        self.policy = policy
        self.layer_width = layer_width
        self.block_locator = block_locator
        self._heap: list[tuple[float, int, _ScheduledEvent]] = []
        self._sequence = 0
        self._counts: list[int] = []
        self._end_time = 0.0
        self._overlaps: set[tuple[int, int]] = set()

    def run(
        self,
        initial_state: DiskState,
        *,
        end_time: float,
        sample_interval: float,
    ) -> ModifiedSimulationResult:
        if end_time <= 0 or sample_interval <= 0:
            raise ValueError("end_time and sample_interval must be positive")
        validate_state_geometry(initial_state, self.domain)
        state = initial_state.copy()
        initial_mass = state.total_mass
        initial_energy = state.kinetic_energy
        initial_momentum = state.momentum
        tracker = MoleculeTracker(tuple(state.particle_ids))

        self._heap = []
        self._sequence = 0
        self._counts = [0] * state.particle_count
        self._end_time = end_time
        self._overlaps = set()
        current_time = 0.0
        stale_events = 0
        collision_log: list[CollisionEvent] = []
        encounter_log: list[EncounterEvent] = []
        exit_log: list[OverlapExitEvent] = []
        snapshots = [Snapshot(0.0, state.copy())]
        maximum_overlaps = 0
        self._schedule_all(state, current_time)

        sample_times = _sample_times(end_time, sample_interval)
        sample_index = 1
        while sample_index < len(sample_times):
            next_sample = sample_times[sample_index]
            scheduled, popped_stale = self._peek_valid_event()
            stale_events += popped_stale
            if scheduled is None or scheduled.time > next_sample + _TIME_EPS:
                self._advance(state, next_sample - current_time)
                current_time = next_sample
                snapshots.append(Snapshot(current_time, state.copy()))
                sample_index += 1
                continue

            heapq.heappop(self._heap)
            if scheduled.time < current_time - _TIME_EPS:
                raise RuntimeError("event queue produced time reversal")
            self._advance(state, max(0.0, scheduled.time - current_time))
            current_time = scheduled.time
            pair = (scheduled.particle_a, scheduled.particle_b)
            if scheduled.kind == "pair_entry":
                encounter = self._resolve_entry(
                    state,
                    scheduled,
                    current_time,
                    tracker,
                    encounter_index=len(encounter_log),
                    collision_log=collision_log,
                )
                encounter_log.append(encounter)
                if encounter.decision is EncounterDecision.SUPPRESS:
                    self._overlaps.add(pair)
                    maximum_overlaps = max(maximum_overlaps, len(self._overlaps))
            elif scheduled.kind == "overlap_exit":
                if pair not in self._overlaps:
                    raise RuntimeError("valid overlap-exit event has no active overlap")
                self._overlaps.remove(pair)
                exit_log.append(
                    OverlapExitEvent(
                        time=current_time,
                        particle_a=state.particle_ids[pair[0]],
                        particle_b=state.particle_ids[pair[1]],
                    )
                )
            else:
                raise AssertionError(f"unknown event kind: {scheduled.kind}")

            affected = (scheduled.particle_a, scheduled.particle_b)
            for particle in affected:
                self._counts[particle] += 1
            self._reschedule_affected(state, current_time, affected)

        diagnostics = SolverDiagnostics(
            initial_mass=initial_mass,
            final_mass=state.total_mass,
            initial_energy=initial_energy,
            final_energy=state.kinetic_energy,
            initial_momentum=initial_momentum,
            final_momentum=state.momentum,
            particle_collision_count=len(collision_log),
            boundary_collision_count=0,
            stale_event_count=stale_events,
        )
        simulation = SimulationResult(
            backend=f"{self.name}:{self.policy.name}",
            event_semantics="admissible_collision_overlap",
            snapshots=tuple(snapshots),
            collision_events=tuple(collision_log),
            diagnostics=diagnostics,
        )
        return ModifiedSimulationResult(
            policy_name=self.policy.name,
            layer_width=self.layer_width,
            simulation=simulation,
            encounter_events=tuple(encounter_log),
            overlap_exit_events=tuple(exit_log),
            maximum_simultaneous_overlaps=maximum_overlaps,
        )

    def _schedule_all(self, state: DiskState, now: float) -> None:
        for left in range(state.particle_count):
            for right in range(left + 1, state.particle_count):
                self._schedule_pair(state, left, right, now)

    def _reschedule_affected(
        self,
        state: DiskState,
        now: float,
        affected: tuple[int, ...],
    ) -> None:
        scheduled_pairs: set[tuple[int, int]] = set()
        for particle in affected:
            for other in range(state.particle_count):
                if particle == other:
                    continue
                pair = (min(particle, other), max(particle, other))
                if pair in scheduled_pairs:
                    continue
                scheduled_pairs.add(pair)
                self._schedule_pair(state, pair[0], pair[1], now)

    def _schedule_pair(self, state: DiskState, left: int, right: int, now: float) -> None:
        pair = (left, right)
        if pair in self._overlaps:
            prediction = self._overlap_exit_prediction(
                state, left, right, self._end_time - now
            )
            kind = "overlap_exit"
        else:
            prediction = self._pair_entry_prediction(
                state, left, right, self._end_time - now
            )
            kind = "pair_entry"
        if prediction is None:
            return
        dt, normal = prediction
        self._push(
            time=now + dt,
            kind=kind,
            particle_a=left,
            particle_b=right,
            normal=normal,
        )

    def _pair_entry_prediction(
        self,
        state: DiskState,
        left: int,
        right: int,
        horizon: float,
    ) -> tuple[float, tuple[float, float]] | None:
        pa = state.positions[left]
        pb = state.positions[right]
        va = state.velocities[left]
        vb = state.velocities[right]
        dv = (vb[0] - va[0], vb[1] - va[1])
        speed2 = dv[0] * dv[0] + dv[1] * dv[1]
        if speed2 <= _TIME_EPS:
            return None
        contact = state.radii[left] + state.radii[right]
        best: tuple[float, tuple[float, float]] | None = None
        for shift_x, shift_y in self._periodic_shifts(pa, pb, dv, horizon):
            rx = pb[0] - pa[0] + shift_x * self.domain.width
            ry = pb[1] - pa[1] + shift_y * self.domain.height
            b = rx * dv[0] + ry * dv[1]
            c = rx * rx + ry * ry - contact * contact
            if c < -_CONTACT_EPS:
                raise RuntimeError(
                    "untracked overlap while scheduling particles "
                    f"{state.particle_ids[left]} and {state.particle_ids[right]}"
                )
            if b >= -_TIME_EPS:
                continue
            discriminant = b * b - speed2 * c
            if discriminant <= 0:
                continue
            dt = (-b - sqrt(discriminant)) / speed2
            candidate = self._prediction_candidate(rx, ry, dv, dt, horizon)
            if candidate is not None and (best is None or candidate[0] < best[0]):
                best = candidate
        return best

    def _overlap_exit_prediction(
        self,
        state: DiskState,
        left: int,
        right: int,
        horizon: float,
    ) -> tuple[float, tuple[float, float]] | None:
        pa = state.positions[left]
        pb = state.positions[right]
        va = state.velocities[left]
        vb = state.velocities[right]
        dv = (vb[0] - va[0], vb[1] - va[1])
        speed2 = dv[0] * dv[0] + dv[1] * dv[1]
        if speed2 <= _TIME_EPS:
            return None
        contact = state.radii[left] + state.radii[right]
        best: tuple[float, tuple[float, float]] | None = None
        for shift_x, shift_y in self._periodic_shifts(pa, pb, dv, horizon):
            rx = pb[0] - pa[0] + shift_x * self.domain.width
            ry = pb[1] - pa[1] + shift_y * self.domain.height
            c = rx * rx + ry * ry - contact * contact
            if c > _CONTACT_EPS:
                continue
            b = rx * dv[0] + ry * dv[1]
            discriminant = b * b - speed2 * c
            if discriminant < 0:
                continue
            dt = (-b + sqrt(max(0.0, discriminant))) / speed2
            candidate = self._prediction_candidate(rx, ry, dv, dt, horizon)
            if candidate is not None and (best is None or candidate[0] < best[0]):
                best = candidate
        return best

    def _prediction_candidate(
        self,
        rx: float,
        ry: float,
        dv: tuple[float, float],
        dt: float,
        horizon: float,
    ) -> tuple[float, tuple[float, float]] | None:
        if dt <= _TIME_EPS or dt > horizon + _TIME_EPS:
            return None
        cx = rx + dv[0] * dt
        cy = ry + dv[1] * dt
        distance = hypot(cx, cy)
        if distance <= 0:
            return None
        return (dt, (cx / distance, cy / distance))

    def _periodic_shifts(
        self,
        pa: tuple[float, float],
        pb: tuple[float, float],
        dv: tuple[float, float],
        horizon: float,
    ) -> tuple[tuple[int, int], ...]:
        shifts_x = _periodic_shift_range(pb[0] - pa[0], dv[0], self.domain.width, horizon)
        shifts_y = _periodic_shift_range(
            pb[1] - pa[1], dv[1], self.domain.height, horizon
        )
        return tuple((shift_x, shift_y) for shift_x in shifts_x for shift_y in shifts_y)

    def _resolve_entry(
        self,
        state: DiskState,
        event: _ScheduledEvent,
        time: float,
        tracker: MoleculeTracker,
        *,
        encounter_index: int,
        collision_log: list[CollisionEvent],
    ) -> EncounterEvent:
        left = event.particle_a
        right = event.particle_b
        particle_a = state.particle_ids[left]
        particle_b = state.particle_ids[right]
        normal = (event.normal_x, event.normal_y)
        pre_a = state.velocities[left]
        pre_b = state.velocities[right]
        incoming_speed = (pre_a[0] - pre_b[0]) * normal[0] + (
            pre_a[1] - pre_b[1]
        ) * normal[1]
        layer = min(int(time / self.layer_width), int(self._end_time / self.layer_width))
        context = EncounterContext(
            time=time,
            layer=layer,
            particle_a=particle_a,
            particle_b=particle_b,
            encounter_index=encounter_index,
        )
        decision = self.policy.decide(context, tracker)
        component_a = tracker.component(particle_a)
        component_b = tracker.component(particle_b)
        predecessor_a, predecessor_b = tracker.predecessors(particle_a, particle_b)
        pair_multiplicity = tracker.next_pair_multiplicity(particle_a, particle_b)
        block_id = self._block_id(state, left, normal)
        component_after = None
        if decision.decision is EncounterDecision.ACCEPT:
            collision_log.append(
                self._resolve_collision(state, event, time, block_id, incoming_speed)
            )
            component_after = tracker.accept_collision(
                particle_a, particle_b, event_id=encounter_index
            )
        post_a = state.velocities[left]
        post_b = state.velocities[right]
        return EncounterEvent(
            event_id=encounter_index,
            time=time,
            layer=layer,
            particle_a=particle_a,
            particle_b=particle_b,
            block_id=block_id,
            contact_normal=normal,
            incoming_relative_normal_velocity=incoming_speed,
            pre_velocity_a=pre_a,
            pre_velocity_b=pre_b,
            post_velocity_a=post_a,
            post_velocity_b=post_b,
            decision=decision.decision,
            reason=decision.reason,
            predecessor_event_a=predecessor_a,
            predecessor_event_b=predecessor_b,
            component_a_before=component_a.component_id,
            component_b_before=component_b.component_id,
            component_a_size_before=component_a.size,
            component_b_size_before=component_b.size,
            component_a_cycle_rank_before=component_a.cycle_rank,
            component_b_cycle_rank_before=component_b.cycle_rank,
            component_after=(component_after.component_id if component_after else None),
            component_size_after=(component_after.size if component_after else None),
            component_cycle_rank_after=(
                component_after.cycle_rank if component_after else None
            ),
            pair_multiplicity=pair_multiplicity,
        )

    def _resolve_collision(
        self,
        state: DiskState,
        event: _ScheduledEvent,
        time: float,
        block_id: str,
        incoming_speed: float,
    ) -> CollisionEvent:
        left = event.particle_a
        right = event.particle_b
        normal = (event.normal_x, event.normal_y)
        va = state.velocities[left]
        vb = state.velocities[right]
        if incoming_speed < -1.0e-9:
            raise RuntimeError("valid collision event is separating")
        inverse_mass = 1.0 / state.masses[left] + 1.0 / state.masses[right]
        impulse = 2.0 * incoming_speed / inverse_mass
        state.velocities[left] = (
            va[0] - impulse * normal[0] / state.masses[left],
            va[1] - impulse * normal[1] / state.masses[left],
        )
        state.velocities[right] = (
            vb[0] + impulse * normal[0] / state.masses[right],
            vb[1] + impulse * normal[1] / state.masses[right],
        )
        return CollisionEvent(
            time=time,
            particle_a=state.particle_ids[left],
            particle_b=state.particle_ids[right],
            block_id=block_id,
            pre_velocity_a=(*va, 0.0),
            pre_velocity_b=(*vb, 0.0),
            post_velocity_a=(*state.velocities[left], 0.0),
            post_velocity_b=(*state.velocities[right], 0.0),
            contact_normal=normal,
            incoming_relative_normal_velocity=incoming_speed,
        )

    def _block_id(
        self,
        state: DiskState,
        left: int,
        normal: tuple[float, float],
    ) -> str:
        contact_point = self.domain.wrap(
            (
                state.positions[left][0] + normal[0] * state.radii[left],
                state.positions[left][1] + normal[1] * state.radii[left],
            )
        )
        return self.block_locator(contact_point) if self.block_locator else "domain"

    def _push(
        self,
        *,
        time: float,
        kind: str,
        particle_a: int,
        particle_b: int,
        normal: tuple[float, float],
    ) -> None:
        event = _ScheduledEvent(
            time=time,
            sequence=self._sequence,
            kind=kind,
            particle_a=particle_a,
            particle_b=particle_b,
            count_a=self._counts[particle_a],
            count_b=self._counts[particle_b],
            normal_x=normal[0],
            normal_y=normal[1],
        )
        self._sequence += 1
        heapq.heappush(self._heap, event.heap_key())

    def _peek_valid_event(self) -> tuple[_ScheduledEvent | None, int]:
        stale = 0
        while self._heap:
            _, _, event = self._heap[0]
            if (
                event.count_a != self._counts[event.particle_a]
                or event.count_b != self._counts[event.particle_b]
            ):
                heapq.heappop(self._heap)
                stale += 1
                continue
            return event, stale
        return None, stale

    def _advance(self, state: DiskState, dt: float) -> None:
        if dt < -_TIME_EPS:
            raise RuntimeError("cannot advance state backward")
        if dt <= 0:
            return
        state.positions = [
            self.domain.wrap(
                (position[0] + velocity[0] * dt, position[1] + velocity[1] * dt)
            )
            for position, velocity in zip(state.positions, state.velocities, strict=True)
        ]


def _sample_times(end_time: float, interval: float) -> list[float]:
    count = floor(end_time / interval + _TIME_EPS)
    times = [index * interval for index in range(count + 1)]
    if not times or end_time - times[-1] > _TIME_EPS:
        times.append(end_time)
    else:
        times[-1] = end_time
    return times


def _periodic_shift_range(
    displacement: float,
    relative_velocity: float,
    period: float,
    horizon: float,
) -> tuple[int, ...]:
    finish = displacement + relative_velocity * max(0.0, horizon)
    low = min(displacement, finish)
    high = max(displacement, finish)
    minimum = floor(-high / period) - 1
    maximum = ceil(-low / period) + 1
    return tuple(range(minimum, maximum + 1))
