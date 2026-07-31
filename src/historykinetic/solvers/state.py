"""Small, dependency-free state types for the two-dimensional reference solvers.

These types intentionally favor clarity over throughput.  They are the executable
physics reference used to validate future native/GPU implementations; production
particle arrays remain an artifact/backend concern.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import hypot, isfinite, pi

Vec2 = tuple[float, float]


class BoundaryKind(StrEnum):
    PERIODIC = "periodic"
    REFLECTIVE = "reflective"


@dataclass(frozen=True, slots=True)
class CircleObstacle:
    obstacle_id: str
    center: Vec2
    radius: float

    def __post_init__(self) -> None:
        if not self.obstacle_id:
            raise ValueError("obstacle_id must not be empty")
        if self.radius <= 0 or not isfinite(self.radius):
            raise ValueError("obstacle radius must be finite and positive")
        if not all(isfinite(value) for value in self.center):
            raise ValueError("obstacle center must be finite")


@dataclass(frozen=True, slots=True)
class Domain2D:
    lower: Vec2
    upper: Vec2
    boundary: BoundaryKind
    obstacles: tuple[CircleObstacle, ...] = ()

    def __post_init__(self) -> None:
        if not all(isfinite(value) for value in (*self.lower, *self.upper)):
            raise ValueError("domain bounds must be finite")
        if self.upper[0] <= self.lower[0] or self.upper[1] <= self.lower[1]:
            raise ValueError("domain upper bounds must exceed lower bounds")
        if self.boundary is BoundaryKind.PERIODIC and self.obstacles:
            raise ValueError("periodic reference domains do not support internal obstacles")
        for obstacle in self.obstacles:
            cx, cy = obstacle.center
            if (
                cx - obstacle.radius <= self.lower[0]
                or cx + obstacle.radius >= self.upper[0]
                or cy - obstacle.radius <= self.lower[1]
                or cy + obstacle.radius >= self.upper[1]
            ):
                raise ValueError(f"obstacle {obstacle.obstacle_id} must lie inside the domain")

    @property
    def width(self) -> float:
        return self.upper[0] - self.lower[0]

    @property
    def height(self) -> float:
        return self.upper[1] - self.lower[1]

    @property
    def area(self) -> float:
        return self.width * self.height - sum(
            pi * obstacle.radius * obstacle.radius for obstacle in self.obstacles
        )

    def contains_disk(self, position: Vec2, radius: float, *, tolerance: float = 1.0e-12) -> bool:
        x, y = position
        if (
            x < self.lower[0] + radius - tolerance
            or x > self.upper[0] - radius + tolerance
            or y < self.lower[1] + radius - tolerance
            or y > self.upper[1] - radius + tolerance
        ):
            return False
        return all(
            hypot(x - obstacle.center[0], y - obstacle.center[1])
            >= obstacle.radius + radius - tolerance
            for obstacle in self.obstacles
        )

    def wrap(self, position: Vec2) -> Vec2:
        if self.boundary is not BoundaryKind.PERIODIC:
            return position
        return (
            self.lower[0] + (position[0] - self.lower[0]) % self.width,
            self.lower[1] + (position[1] - self.lower[1]) % self.height,
        )


@dataclass(slots=True)
class DiskState:
    positions: list[Vec2]
    velocities: list[Vec2]
    radii: list[float]
    masses: list[float]
    particle_ids: list[int]
    weights: list[float]

    def __post_init__(self) -> None:
        lengths = {
            len(self.positions),
            len(self.velocities),
            len(self.radii),
            len(self.masses),
            len(self.particle_ids),
            len(self.weights),
        }
        if len(lengths) != 1:
            raise ValueError("all particle arrays must have identical lengths")
        if len(set(self.particle_ids)) != len(self.particle_ids):
            raise ValueError("particle IDs must be unique")
        if any(radius <= 0 or not isfinite(radius) for radius in self.radii):
            raise ValueError("particle radii must be finite and positive")
        if any(mass <= 0 or not isfinite(mass) for mass in self.masses):
            raise ValueError("particle masses must be finite and positive")
        if any(weight <= 0 or not isfinite(weight) for weight in self.weights):
            raise ValueError("particle weights must be finite and positive")
        if not all(
            isfinite(value)
            for vector in (*self.positions, *self.velocities)
            for value in vector
        ):
            raise ValueError("positions and velocities must be finite")

    @property
    def particle_count(self) -> int:
        return len(self.positions)

    def copy(self) -> DiskState:
        return DiskState(
            positions=list(self.positions),
            velocities=list(self.velocities),
            radii=list(self.radii),
            masses=list(self.masses),
            particle_ids=list(self.particle_ids),
            weights=list(self.weights),
        )

    @property
    def total_mass(self) -> float:
        return sum(mass * weight for mass, weight in zip(self.masses, self.weights, strict=True))

    @property
    def momentum(self) -> Vec2:
        px = 0.0
        py = 0.0
        for velocity, mass, weight in zip(
            self.velocities, self.masses, self.weights, strict=True
        ):
            physical_mass = mass * weight
            px += physical_mass * velocity[0]
            py += physical_mass * velocity[1]
        return (px, py)

    @property
    def kinetic_energy(self) -> float:
        return 0.5 * sum(
            mass * weight * (velocity[0] * velocity[0] + velocity[1] * velocity[1])
            for velocity, mass, weight in zip(
                self.velocities, self.masses, self.weights, strict=True
            )
        )


@dataclass(frozen=True, slots=True)
class Snapshot:
    time: float
    state: DiskState

    def __post_init__(self) -> None:
        if self.time < 0 or not isfinite(self.time):
            raise ValueError("snapshot time must be finite and non-negative")


def minimum_image(displacement: Vec2, domain: Domain2D) -> Vec2:
    """Return the nearest periodic image displacement."""

    if domain.boundary is not BoundaryKind.PERIODIC:
        return displacement
    dx, dy = displacement
    dx -= round(dx / domain.width) * domain.width
    dy -= round(dy / domain.height) * domain.height
    return (dx, dy)


def validate_state_geometry(
    state: DiskState,
    domain: Domain2D,
    *,
    overlap_tolerance: float = 1.0e-10,
) -> None:
    for index, (position, radius) in enumerate(
        zip(state.positions, state.radii, strict=True)
    ):
        if domain.boundary is BoundaryKind.REFLECTIVE and not domain.contains_disk(
            position, radius, tolerance=overlap_tolerance
        ):
            raise ValueError(f"particle {state.particle_ids[index]} is outside valid geometry")

    for left in range(state.particle_count):
        for right in range(left + 1, state.particle_count):
            raw = (
                state.positions[right][0] - state.positions[left][0],
                state.positions[right][1] - state.positions[left][1],
            )
            dx, dy = minimum_image(raw, domain)
            minimum_distance = state.radii[left] + state.radii[right]
            if hypot(dx, dy) < minimum_distance - overlap_tolerance:
                raise ValueError(
                    f"particles {state.particle_ids[left]} and "
                    f"{state.particle_ids[right]} overlap"
                )
