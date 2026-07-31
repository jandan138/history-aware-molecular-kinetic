"""Minimal two-dimensional Boltzmann DSMC baseline.

The implementation shares initial ensembles, geometry, sampling times, and
observables with the EDMD reference while deliberately keeping stochastic
collisions semantically separate from geometric collision history.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from math import floor, hypot, sqrt

from historykinetic.contracts import CollisionEvent
from historykinetic.solvers.result import SimulationResult, SolverDiagnostics
from historykinetic.solvers.state import BoundaryKind, DiskState, Domain2D, Snapshot

_EPS = 1.0e-12


class HardDiskDSMC:
    semantic_version = "0.1.0"
    name = "python_boltzmann_dsmc_reference"

    def __init__(
        self,
        domain: Domain2D,
        *,
        cells_x: int,
        cells_y: int,
        time_step: float,
        seed: int,
        block_locator: Callable[[tuple[float, float]], str] | None = None,
    ) -> None:
        if cells_x <= 0 or cells_y <= 0:
            raise ValueError("DSMC cell dimensions must be positive")
        if time_step <= 0:
            raise ValueError("DSMC time_step must be positive")
        self.domain = domain
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.time_step = time_step
        self.seed = seed
        self.block_locator = block_locator
        self.cell_width = domain.width / cells_x
        self.cell_height = domain.height / cells_y

    def run(
        self,
        initial_state: DiskState,
        *,
        end_time: float,
        sample_interval: float,
    ) -> SimulationResult:
        if end_time <= 0 or sample_interval <= 0:
            raise ValueError("end_time and sample_interval must be positive")
        state = initial_state.copy()
        rng = random.Random(self.seed)
        initial_mass = state.total_mass
        initial_energy = state.kinetic_energy
        initial_momentum = state.momentum
        snapshots = [Snapshot(0.0, state.copy())]
        collision_log: list[CollisionEvent] = []
        boundary_collisions = 0
        current_time = 0.0
        next_sample = min(sample_interval, end_time)

        while current_time < end_time - _EPS:
            step = min(self.time_step, next_sample - current_time, end_time - current_time)
            for particle in range(state.particle_count):
                boundary_collisions += self._transport_particle(state, particle, step)
            collision_log.extend(self._collide_cells(state, current_time, step, rng))
            current_time += step
            if current_time >= next_sample - _EPS:
                current_time = next_sample
                snapshots.append(Snapshot(current_time, state.copy()))
                if next_sample >= end_time - _EPS:
                    break
                next_sample = min(end_time, next_sample + sample_interval)

        collision_log.sort(key=lambda event: event.time)
        diagnostics = SolverDiagnostics(
            initial_mass=initial_mass,
            final_mass=state.total_mass,
            initial_energy=initial_energy,
            final_energy=state.kinetic_energy,
            initial_momentum=initial_momentum,
            final_momentum=state.momentum,
            particle_collision_count=len(collision_log),
            boundary_collision_count=boundary_collisions,
        )
        return SimulationResult(
            backend=self.name,
            event_semantics="kinetic_collision",
            snapshots=tuple(snapshots),
            collision_events=tuple(collision_log),
            diagnostics=diagnostics,
        )

    def _transport_particle(self, state: DiskState, particle: int, duration: float) -> int:
        position = state.positions[particle]
        velocity = state.velocities[particle]
        radius = state.radii[particle]
        if self.domain.boundary is BoundaryKind.PERIODIC:
            state.positions[particle] = self.domain.wrap(
                (
                    position[0] + velocity[0] * duration,
                    position[1] + velocity[1] * duration,
                )
            )
            return 0

        remaining = duration
        collision_count = 0
        for _ in range(32):
            if remaining <= _EPS:
                break
            event = self._next_geometry_event(position, velocity, radius, remaining)
            if event is None:
                position = (
                    position[0] + velocity[0] * remaining,
                    position[1] + velocity[1] * remaining,
                )
                remaining = 0.0
                break
            travel, normal = event
            position = (
                position[0] + velocity[0] * travel,
                position[1] + velocity[1] * travel,
            )
            projection = velocity[0] * normal[0] + velocity[1] * normal[1]
            velocity = (
                velocity[0] - 2.0 * projection * normal[0],
                velocity[1] - 2.0 * projection * normal[1],
            )
            remaining -= travel
            collision_count += 1
            position = (
                position[0] + normal[0] * 1.0e-11,
                position[1] + normal[1] * 1.0e-11,
            )
        else:
            raise RuntimeError("too many geometry reflections in one DSMC transport step")

        state.positions[particle] = position
        state.velocities[particle] = velocity
        return collision_count

    def _next_geometry_event(
        self,
        position: tuple[float, float],
        velocity: tuple[float, float],
        radius: float,
        horizon: float,
    ) -> tuple[float, tuple[float, float]] | None:
        candidates: list[tuple[float, tuple[float, float]]] = []
        x, y = position
        vx, vy = velocity
        if vx > _EPS:
            candidates.append(((self.domain.upper[0] - radius - x) / vx, (-1.0, 0.0)))
        elif vx < -_EPS:
            candidates.append(((self.domain.lower[0] + radius - x) / vx, (1.0, 0.0)))
        if vy > _EPS:
            candidates.append(((self.domain.upper[1] - radius - y) / vy, (0.0, -1.0)))
        elif vy < -_EPS:
            candidates.append(((self.domain.lower[1] + radius - y) / vy, (0.0, 1.0)))

        speed2 = vx * vx + vy * vy
        if speed2 > _EPS:
            for obstacle in self.domain.obstacles:
                rx = x - obstacle.center[0]
                ry = y - obstacle.center[1]
                b = rx * vx + ry * vy
                contact = obstacle.radius + radius
                c = rx * rx + ry * ry - contact * contact
                discriminant = b * b - speed2 * c
                if b >= -_EPS or discriminant <= 0:
                    continue
                travel = (-b - sqrt(discriminant)) / speed2
                if travel <= _EPS:
                    continue
                cx = rx + vx * travel
                cy = ry + vy * travel
                distance = hypot(cx, cy)
                candidates.append((travel, (cx / distance, cy / distance)))

        valid = [candidate for candidate in candidates if _EPS < candidate[0] <= horizon + _EPS]
        return min(valid, key=lambda candidate: candidate[0]) if valid else None

    def _collide_cells(
        self,
        state: DiskState,
        start_time: float,
        time_step: float,
        rng: random.Random,
    ) -> list[CollisionEvent]:
        cells: dict[tuple[int, int], list[int]] = {}
        for particle, position in enumerate(state.positions):
            ix = min(
                self.cells_x - 1,
                max(0, int((position[0] - self.domain.lower[0]) / self.cell_width)),
            )
            iy = min(
                self.cells_y - 1,
                max(0, int((position[1] - self.domain.lower[1]) / self.cell_height)),
            )
            cells.setdefault((ix, iy), []).append(particle)

        events: list[CollisionEvent] = []
        cell_area = self.cell_width * self.cell_height
        for members in cells.values():
            if len(members) < 2:
                continue
            maximum_relative_speed = max(
                hypot(
                    state.velocities[left][0] - state.velocities[right][0],
                    state.velocities[left][1] - state.velocities[right][1],
                )
                for offset, left in enumerate(members)
                for right in members[offset + 1 :]
            )
            if maximum_relative_speed <= _EPS:
                continue
            maximum_cross_section = max(
                2.0 * (state.radii[left] + state.radii[right])
                for offset, left in enumerate(members)
                for right in members[offset + 1 :]
            )
            maximum_weight = max(state.weights[index] for index in members)
            pair_count = len(members) * (len(members) - 1) / 2.0
            expected_candidates = (
                pair_count
                * maximum_cross_section
                * maximum_relative_speed
                * maximum_weight
                * time_step
                / cell_area
            )
            candidate_count = floor(expected_candidates)
            if rng.random() < expected_candidates - candidate_count:
                candidate_count += 1

            for _ in range(candidate_count):
                left, right = rng.sample(members, 2)
                va = state.velocities[left]
                vb = state.velocities[right]
                gx = va[0] - vb[0]
                gy = va[1] - vb[1]
                relative_speed = hypot(gx, gy)
                cross_section = 2.0 * (state.radii[left] + state.radii[right])
                acceptance = (
                    relative_speed
                    * cross_section
                    * max(state.weights[left], state.weights[right])
                    / (
                        maximum_relative_speed
                        * maximum_cross_section
                        * maximum_weight
                    )
                )
                if rng.random() > min(1.0, acceptance) or relative_speed <= _EPS:
                    continue
                pre_left = (va[0], va[1], 0.0)
                pre_right = (vb[0], vb[1], 0.0)
                impact = rng.uniform(-1.0, 1.0)
                head_on = sqrt(max(0.0, 1.0 - impact * impact))
                unit_g = (gx / relative_speed, gy / relative_speed)
                perpendicular = (-unit_g[1], unit_g[0])
                normal = (
                    head_on * unit_g[0] + impact * perpendicular[0],
                    head_on * unit_g[1] + impact * perpendicular[1],
                )
                relative_normal_speed = gx * normal[0] + gy * normal[1]
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
                midpoint = self.domain.wrap(
                    (
                        0.5 * (state.positions[left][0] + state.positions[right][0]),
                        0.5 * (state.positions[left][1] + state.positions[right][1]),
                    )
                )
                block_id = (
                    self.block_locator(midpoint)
                    if self.block_locator is not None
                    else "domain"
                )
                events.append(
                    CollisionEvent(
                        time=start_time + rng.random() * time_step,
                        particle_a=state.particle_ids[left],
                        particle_b=state.particle_ids[right],
                        block_id=block_id,
                        pre_velocity_a=pre_left,
                        pre_velocity_b=pre_right,
                        post_velocity_a=(*state.velocities[left], 0.0),
                        post_velocity_b=(*state.velocities[right], 0.0),
                    )
                )
        return events
