"""Correctness-first event-driven molecular dynamics for elastic hard disks."""

from __future__ import annotations

import heapq
from collections.abc import Callable
from dataclasses import dataclass
from math import ceil, floor, hypot, sqrt

from historykinetic.contracts import CollisionEvent
from historykinetic.solvers.result import (
    GeometryCollisionEvent,
    SimulationResult,
    SolverDiagnostics,
)
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


class HardDiskEDMD:
    """A deterministic O(N)-reschedule EDMD reference.

    The implementation uses event invalidation counters and exact quadratic
    collision times.  It is deliberately small and auditable, not optimized for
    the production particle counts targeted by the native compute plane.
    """

    semantic_version = "0.1.0"
    name = "python_edmd_reference"

    def __init__(
        self,
        domain: Domain2D,
        *,
        block_locator: Callable[[tuple[float, float]], str] | None = None,
    ) -> None:
        self.domain = domain
        self.block_locator = block_locator
        self._heap: list[tuple[float, int, _ScheduledEvent]] = []
        self._sequence = 0
        self._counts: list[int] = []
        self._end_time = 0.0

    def run(
        self,
        initial_state: DiskState,
        *,
        end_time: float,
        sample_interval: float,
    ) -> SimulationResult:
        if end_time <= 0 or sample_interval <= 0:
            raise ValueError("end_time and sample_interval must be positive")
        validate_state_geometry(initial_state, self.domain)
        state = initial_state.copy()
        initial_mass = state.total_mass
        initial_energy = state.kinetic_energy
        initial_momentum = state.momentum

        self._heap = []
        self._sequence = 0
        self._counts = [0] * state.particle_count
        self._end_time = end_time
        current_time = 0.0
        particle_collisions = 0
        boundary_collisions = 0
        stale_events = 0
        collision_log: list[CollisionEvent] = []
        geometry_collision_log: list[GeometryCollisionEvent] = []
        snapshots = [Snapshot(0.0, state.copy())]
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
            if scheduled.kind == "pair":
                collision_log.append(self._resolve_pair(state, scheduled, current_time))
                particle_collisions += 1
                affected: tuple[int, ...] = (
                    scheduled.particle_a,
                    scheduled.particle_b,
                )
            elif scheduled.kind in {"wall_x", "wall_y", "obstacle"}:
                geometry_collision_log.append(
                    self._resolve_boundary(state, scheduled, current_time)
                )
                boundary_collisions += 1
                affected = (scheduled.particle_a,)
            else:
                raise AssertionError(f"unknown event kind: {scheduled.kind}")

            for particle in affected:
                self._counts[particle] += 1
            self._reschedule_affected(state, current_time, affected)

        validate_state_geometry(state, self.domain, overlap_tolerance=5.0e-9)
        diagnostics = SolverDiagnostics(
            initial_mass=initial_mass,
            final_mass=state.total_mass,
            initial_energy=initial_energy,
            final_energy=state.kinetic_energy,
            initial_momentum=initial_momentum,
            final_momentum=state.momentum,
            particle_collision_count=particle_collisions,
            boundary_collision_count=boundary_collisions,
            stale_event_count=stale_events,
        )
        return SimulationResult(
            backend=self.name,
            event_semantics="geometric_collision",
            snapshots=tuple(snapshots),
            collision_events=tuple(collision_log),
            diagnostics=diagnostics,
            geometry_collision_events=tuple(geometry_collision_log),
        )

    def _schedule_all(self, state: DiskState, now: float) -> None:
        for particle in range(state.particle_count):
            self._schedule_boundaries(state, particle, now)
        for left in range(state.particle_count):
            for right in range(left + 1, state.particle_count):
                self._schedule_pair(state, left, right, now)

    def _reschedule_affected(
        self,
        state: DiskState,
        now: float,
        affected: tuple[int, ...],
    ) -> None:
        affected_set = set(affected)
        for particle in affected:
            self._schedule_boundaries(state, particle, now)
        scheduled_pairs: set[tuple[int, int]] = set()
        for particle in affected:
            for other in range(state.particle_count):
                if particle == other:
                    continue
                pair = (min(particle, other), max(particle, other))
                if pair in scheduled_pairs:
                    continue
                if pair[0] not in affected_set and pair[1] not in affected_set:
                    continue
                scheduled_pairs.add(pair)
                self._schedule_pair(state, pair[0], pair[1], now)

    def _schedule_pair(self, state: DiskState, left: int, right: int, now: float) -> None:
        prediction = self._pair_prediction(state, left, right, self._end_time - now)
        if prediction is None:
            return
        dt, normal = prediction
        self._push(
            time=now + dt,
            kind="pair",
            particle_a=left,
            particle_b=right,
            count_a=self._counts[left],
            count_b=self._counts[right],
            normal=normal,
        )

    def _pair_prediction(
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

        shifts_x: tuple[int, ...] = (0,)
        shifts_y: tuple[int, ...] = (0,)
        if self.domain.boundary is BoundaryKind.PERIODIC:
            shifts_x = _periodic_shift_range(
                pb[0] - pa[0], dv[0], self.domain.width, horizon
            )
            shifts_y = _periodic_shift_range(
                pb[1] - pa[1], dv[1], self.domain.height, horizon
            )

        best: tuple[float, tuple[float, float]] | None = None
        for shift_x in shifts_x:
            for shift_y in shifts_y:
                rx = pb[0] - pa[0] + shift_x * self.domain.width
                ry = pb[1] - pa[1] + shift_y * self.domain.height
                b = rx * dv[0] + ry * dv[1]
                c = rx * rx + ry * ry - contact * contact
                if c < -_CONTACT_EPS:
                    raise RuntimeError(
                        f"overlap detected while scheduling particles "
                        f"{state.particle_ids[left]} and {state.particle_ids[right]}"
                    )
                if b >= -_TIME_EPS:
                    continue
                discriminant = b * b - speed2 * c
                if discriminant <= 0:
                    continue
                dt = (-b - sqrt(discriminant)) / speed2
                if dt <= _TIME_EPS or dt > horizon + _TIME_EPS:
                    continue
                cx = rx + dv[0] * dt
                cy = ry + dv[1] * dt
                distance = hypot(cx, cy)
                if distance <= 0:
                    continue
                candidate = (dt, (cx / distance, cy / distance))
                if best is None or candidate[0] < best[0]:
                    best = candidate
        return best

    def _schedule_boundaries(self, state: DiskState, particle: int, now: float) -> None:
        if self.domain.boundary is BoundaryKind.REFLECTIVE:
            x, y = state.positions[particle]
            vx, vy = state.velocities[particle]
            radius = state.radii[particle]
            if vx > _TIME_EPS:
                dt = (self.domain.upper[0] - radius - x) / vx
                self._push_wall(now, dt, "wall_x", particle, (-1.0, 0.0))
            elif vx < -_TIME_EPS:
                dt = (self.domain.lower[0] + radius - x) / vx
                self._push_wall(now, dt, "wall_x", particle, (1.0, 0.0))
            if vy > _TIME_EPS:
                dt = (self.domain.upper[1] - radius - y) / vy
                self._push_wall(now, dt, "wall_y", particle, (0.0, -1.0))
            elif vy < -_TIME_EPS:
                dt = (self.domain.lower[1] + radius - y) / vy
                self._push_wall(now, dt, "wall_y", particle, (0.0, 1.0))

            for obstacle_index, obstacle in enumerate(self.domain.obstacles):
                rx = x - obstacle.center[0]
                ry = y - obstacle.center[1]
                b = rx * vx + ry * vy
                speed2 = vx * vx + vy * vy
                contact = obstacle.radius + radius
                c = rx * rx + ry * ry - contact * contact
                if b >= -_TIME_EPS or speed2 <= _TIME_EPS:
                    continue
                discriminant = b * b - speed2 * c
                if discriminant <= 0:
                    continue
                dt = (-b - sqrt(discriminant)) / speed2
                if dt <= _TIME_EPS or now + dt > self._end_time + _TIME_EPS:
                    continue
                cx = rx + vx * dt
                cy = ry + vy * dt
                distance = hypot(cx, cy)
                self._push(
                    time=now + dt,
                    kind="obstacle",
                    particle_a=particle,
                    particle_b=obstacle_index,
                    count_a=self._counts[particle],
                    count_b=-1,
                    normal=(cx / distance, cy / distance),
                )

    def _push_wall(
        self,
        now: float,
        dt: float,
        kind: str,
        particle: int,
        normal: tuple[float, float],
    ) -> None:
        if dt <= _TIME_EPS or now + dt > self._end_time + _TIME_EPS:
            return
        self._push(
            time=now + dt,
            kind=kind,
            particle_a=particle,
            particle_b=-1,
            count_a=self._counts[particle],
            count_b=-1,
            normal=normal,
        )

    def _push(
        self,
        *,
        time: float,
        kind: str,
        particle_a: int,
        particle_b: int,
        count_a: int,
        count_b: int,
        normal: tuple[float, float],
    ) -> None:
        event = _ScheduledEvent(
            time=time,
            sequence=self._sequence,
            kind=kind,
            particle_a=particle_a,
            particle_b=particle_b,
            count_a=count_a,
            count_b=count_b,
            normal_x=normal[0],
            normal_y=normal[1],
        )
        self._sequence += 1
        heapq.heappush(self._heap, event.heap_key())

    def _peek_valid_event(self) -> tuple[_ScheduledEvent | None, int]:
        stale = 0
        while self._heap:
            _, _, event = self._heap[0]
            if event.count_a != self._counts[event.particle_a]:
                heapq.heappop(self._heap)
                stale += 1
                continue
            if event.kind == "pair" and event.count_b != self._counts[event.particle_b]:
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
        positions: list[tuple[float, float]] = []
        for position, velocity in zip(state.positions, state.velocities, strict=True):
            positions.append(
                self.domain.wrap(
                    (position[0] + velocity[0] * dt, position[1] + velocity[1] * dt)
                )
            )
        state.positions = positions

    def _resolve_pair(
        self,
        state: DiskState,
        event: _ScheduledEvent,
        time: float,
    ) -> CollisionEvent:
        left = event.particle_a
        right = event.particle_b
        normal = (event.normal_x, event.normal_y)
        va = state.velocities[left]
        vb = state.velocities[right]
        pre_a = (va[0], va[1], 0.0)
        pre_b = (vb[0], vb[1], 0.0)
        relative_normal_speed = (va[0] - vb[0]) * normal[0] + (
            va[1] - vb[1]
        ) * normal[1]
        if relative_normal_speed < -1.0e-9:
            raise RuntimeError("valid collision event is separating")
        inverse_mass = 1.0 / state.masses[left] + 1.0 / state.masses[right]
        impulse = 2.0 * relative_normal_speed / inverse_mass
        state.velocities[left] = (
            va[0] - impulse * normal[0] / state.masses[left],
            va[1] - impulse * normal[1] / state.masses[left],
        )
        state.velocities[right] = (
            vb[0] + impulse * normal[0] / state.masses[right],
            vb[1] + impulse * normal[1] / state.masses[right],
        )
        post_a = (*state.velocities[left], 0.0)
        post_b = (*state.velocities[right], 0.0)
        contact_point = self.domain.wrap(
            (
                state.positions[left][0] + normal[0] * state.radii[left],
                state.positions[left][1] + normal[1] * state.radii[left],
            )
        )
        block_id = (
            self.block_locator(contact_point) if self.block_locator is not None else "domain"
        )
        return CollisionEvent(
            time=time,
            particle_a=state.particle_ids[left],
            particle_b=state.particle_ids[right],
            block_id=block_id,
            pre_velocity_a=pre_a,
            pre_velocity_b=pre_b,
            post_velocity_a=post_a,
            post_velocity_b=post_b,
            contact_normal=normal,
            incoming_relative_normal_velocity=relative_normal_speed,
        )

    def _resolve_boundary(
        self,
        state: DiskState,
        event: _ScheduledEvent,
        time: float,
    ) -> GeometryCollisionEvent:
        particle = event.particle_a
        velocity = state.velocities[particle]
        pre_velocity = velocity
        normal = (event.normal_x, event.normal_y)
        projection = velocity[0] * normal[0] + velocity[1] * normal[1]
        state.velocities[particle] = (
            velocity[0] - 2.0 * projection * normal[0],
            velocity[1] - 2.0 * projection * normal[1],
        )
        if event.kind == "obstacle":
            surface_id = self.domain.obstacles[event.particle_b].obstacle_id
        elif event.kind == "wall_x":
            surface_id = "wall-left" if normal[0] > 0 else "wall-right"
        else:
            surface_id = "wall-bottom" if normal[1] > 0 else "wall-top"
        block_id = (
            self.block_locator(state.positions[particle])
            if self.block_locator is not None
            else "domain"
        )
        return GeometryCollisionEvent(
            time=time,
            particle_id=state.particle_ids[particle],
            block_id=block_id,
            surface_id=surface_id,
            pre_velocity=pre_velocity,
            post_velocity=state.velocities[particle],
        )


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
    start = displacement
    finish = displacement + relative_velocity * max(0.0, horizon)
    low = min(start, finish)
    high = max(start, finish)
    minimum = floor(-high / period) - 1
    maximum = ceil(-low / period) + 1
    return tuple(range(minimum, maximum + 1))
