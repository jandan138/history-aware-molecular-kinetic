"""Shared block observables for exact/kinetic paired comparisons."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot, pi, sqrt

from historykinetic.solvers.state import DiskState, Domain2D, Vec2


@dataclass(frozen=True, slots=True)
class BlockGrid:
    domain: Domain2D
    cells_x: int
    cells_y: int

    def __post_init__(self) -> None:
        if self.cells_x <= 0 or self.cells_y <= 0:
            raise ValueError("block-grid dimensions must be positive")

    @property
    def cell_width(self) -> float:
        return self.domain.width / self.cells_x

    @property
    def cell_height(self) -> float:
        return self.domain.height / self.cells_y

    def index(self, position: Vec2) -> tuple[int, int]:
        ix = min(
            self.cells_x - 1,
            max(0, int((position[0] - self.domain.lower[0]) / self.cell_width)),
        )
        iy = min(
            self.cells_y - 1,
            max(0, int((position[1] - self.domain.lower[1]) / self.cell_height)),
        )
        return (ix, iy)

    def block_id(self, position: Vec2) -> str:
        ix, iy = self.index(position)
        return f"b-{ix:02d}-{iy:02d}"

    def bounds(self, ix: int, iy: int) -> tuple[float, float, float, float]:
        x0 = self.domain.lower[0] + ix * self.cell_width
        y0 = self.domain.lower[1] + iy * self.cell_height
        return (x0, y0, x0 + self.cell_width, y0 + self.cell_height)

    def center(self, ix: int, iy: int) -> Vec2:
        x0, y0, x1, y1 = self.bounds(ix, iy)
        return ((x0 + x1) * 0.5, (y0 + y1) * 0.5)

    def accessible_area(self, ix: int, iy: int, *, samples_per_axis: int = 12) -> float:
        """Deterministic subcell estimate used equally by both representations."""

        x0, y0, x1, y1 = self.bounds(ix, iy)
        if not self.domain.obstacles:
            return (x1 - x0) * (y1 - y0)
        accessible = 0
        total = samples_per_axis * samples_per_axis
        for sy in range(samples_per_axis):
            y = y0 + (sy + 0.5) * (y1 - y0) / samples_per_axis
            for sx in range(samples_per_axis):
                x = x0 + (sx + 0.5) * (x1 - x0) / samples_per_axis
                if all(
                    hypot(x - obstacle.center[0], y - obstacle.center[1])
                    >= obstacle.radius
                    for obstacle in self.domain.obstacles
                ):
                    accessible += 1
        return (x1 - x0) * (y1 - y0) * accessible / total

    def geometry_features(self, ix: int, iy: int) -> dict[str, float]:
        center = self.center(ix, iy)
        wall_distance = min(
            center[0] - self.domain.lower[0],
            self.domain.upper[0] - center[0],
            center[1] - self.domain.lower[1],
            self.domain.upper[1] - center[1],
        )
        obstacle_distance = min(
            (
                hypot(center[0] - obstacle.center[0], center[1] - obstacle.center[1])
                - obstacle.radius
                for obstacle in self.domain.obstacles
            ),
            default=max(self.domain.width, self.domain.height),
        )
        full_area = self.cell_width * self.cell_height
        return {
            "accessible_fraction": self.accessible_area(ix, iy) / full_area,
            "wall_distance": max(0.0, wall_distance),
            "obstacle_distance": max(0.0, obstacle_distance),
            "aspect_ratio": self.domain.width / self.domain.height,
        }


@dataclass(frozen=True, slots=True)
class BlockObservation:
    block_id: str
    time: float
    sample_count: int
    number_density: float
    packing_fraction: float
    mean_velocity_x: float
    mean_velocity_y: float
    temperature: float
    maxwellian_residual: float
    stress_deviator_norm: float
    heat_flux_norm: float
    mean_speed: float
    speed_variance: float

    def state_features(self) -> dict[str, float]:
        return {
            "number_density": self.number_density,
            "packing_fraction": self.packing_fraction,
            "mean_velocity_x": self.mean_velocity_x,
            "mean_velocity_y": self.mean_velocity_y,
            "temperature": self.temperature,
            "maxwellian_residual": self.maxwellian_residual,
            "stress_deviator_norm": self.stress_deviator_norm,
            "heat_flux_norm": self.heat_flux_norm,
            "mean_speed": self.mean_speed,
            "speed_variance": self.speed_variance,
            "sample_count": float(self.sample_count),
        }

    def target_observables(self) -> dict[str, float]:
        return {
            "number_density": self.number_density,
            "mean_velocity_x": self.mean_velocity_x,
            "mean_velocity_y": self.mean_velocity_y,
            "temperature": self.temperature,
            "maxwellian_residual": self.maxwellian_residual,
            "stress_deviator_norm": self.stress_deviator_norm,
            "heat_flux_norm": self.heat_flux_norm,
        }


def observe_blocks(state: DiskState, grid: BlockGrid, time: float) -> tuple[BlockObservation, ...]:
    members: dict[tuple[int, int], list[int]] = {
        (ix, iy): []
        for iy in range(grid.cells_y)
        for ix in range(grid.cells_x)
    }
    for particle, position in enumerate(state.positions):
        members[grid.index(position)].append(particle)

    observations: list[BlockObservation] = []
    for iy in range(grid.cells_y):
        for ix in range(grid.cells_x):
            indices = members[(ix, iy)]
            area = grid.accessible_area(ix, iy)
            observations.append(
                _observe_members(
                    state,
                    indices,
                    block_id=f"b-{ix:02d}-{iy:02d}",
                    time=time,
                    area=area,
                )
            )
    return tuple(observations)


def _observe_members(
    state: DiskState,
    indices: list[int],
    *,
    block_id: str,
    time: float,
    area: float,
) -> BlockObservation:
    if not indices or area <= 0:
        return BlockObservation(
            block_id=block_id,
            time=time,
            sample_count=0,
            number_density=0.0,
            packing_fraction=0.0,
            mean_velocity_x=0.0,
            mean_velocity_y=0.0,
            temperature=0.0,
            maxwellian_residual=0.0,
            stress_deviator_norm=0.0,
            heat_flux_norm=0.0,
            mean_speed=0.0,
            speed_variance=0.0,
        )

    weights = [state.weights[index] for index in indices]
    total_weight = sum(weights)
    total_mass = sum(state.masses[index] * state.weights[index] for index in indices)
    ux = (
        sum(
            state.masses[index] * state.weights[index] * state.velocities[index][0]
            for index in indices
        )
        / total_mass
    )
    uy = (
        sum(
            state.masses[index] * state.weights[index] * state.velocities[index][1]
            for index in indices
        )
        / total_mass
    )
    peculiar = [
        (state.velocities[index][0] - ux, state.velocities[index][1] - uy)
        for index in indices
    ]
    thermal_energy_twice = sum(
        state.masses[index]
        * state.weights[index]
        * (velocity[0] * velocity[0] + velocity[1] * velocity[1])
        for index, velocity in zip(indices, peculiar, strict=True)
    )
    temperature = thermal_energy_twice / (2.0 * total_weight)

    pxx = sum(
        state.masses[index] * state.weights[index] * velocity[0] * velocity[0]
        for index, velocity in zip(indices, peculiar, strict=True)
    ) / area
    pyy = sum(
        state.masses[index] * state.weights[index] * velocity[1] * velocity[1]
        for index, velocity in zip(indices, peculiar, strict=True)
    ) / area
    pxy = sum(
        state.masses[index] * state.weights[index] * velocity[0] * velocity[1]
        for index, velocity in zip(indices, peculiar, strict=True)
    ) / area
    pressure = 0.5 * (pxx + pyy)
    stress_norm = sqrt(
        (pxx - pressure) ** 2 + (pyy - pressure) ** 2 + 2.0 * pxy * pxy
    )

    qx = 0.5 * sum(
        state.masses[index]
        * state.weights[index]
        * (velocity[0] * velocity[0] + velocity[1] * velocity[1])
        * velocity[0]
        for index, velocity in zip(indices, peculiar, strict=True)
    ) / area
    qy = 0.5 * sum(
        state.masses[index]
        * state.weights[index]
        * (velocity[0] * velocity[0] + velocity[1] * velocity[1])
        * velocity[1]
        for index, velocity in zip(indices, peculiar, strict=True)
    ) / area

    speeds = [hypot(*state.velocities[index]) for index in indices]
    mean_speed = sum(
        state.weights[index] * speed for index, speed in zip(indices, speeds, strict=True)
    ) / total_weight
    speed_variance = sum(
        state.weights[index] * (speed - mean_speed) ** 2
        for index, speed in zip(indices, speeds, strict=True)
    ) / total_weight

    c2 = [
        velocity[0] * velocity[0] + velocity[1] * velocity[1] for velocity in peculiar
    ]
    mean_c2 = sum(
        state.weights[index] * value for index, value in zip(indices, c2, strict=True)
    ) / total_weight
    mean_c4 = sum(
        state.weights[index] * value * value
        for index, value in zip(indices, c2, strict=True)
    ) / total_weight
    maxwell_residual = (
        abs(mean_c4 / (2.0 * mean_c2 * mean_c2) - 1.0) if mean_c2 > 1.0e-30 else 0.0
    )

    packing = sum(
        state.weights[index] * pi * state.radii[index] ** 2 for index in indices
    ) / area
    return BlockObservation(
        block_id=block_id,
        time=time,
        sample_count=len(indices),
        number_density=total_weight / area,
        packing_fraction=min(packing, 1.0 - 1.0e-15),
        mean_velocity_x=ux,
        mean_velocity_y=uy,
        temperature=temperature,
        maxwellian_residual=maxwell_residual,
        stress_deviator_norm=stress_norm,
        heat_flux_norm=hypot(qx, qy),
        mean_speed=mean_speed,
        speed_variance=speed_variance,
    )
