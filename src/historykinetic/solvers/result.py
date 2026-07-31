from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Literal

from historykinetic.contracts import CollisionEvent
from historykinetic.solvers.state import Snapshot


@dataclass(frozen=True, slots=True)
class GeometryCollisionEvent:
    time: float
    particle_id: int
    block_id: str
    surface_id: str
    pre_velocity: tuple[float, float]
    post_velocity: tuple[float, float]


@dataclass(frozen=True, slots=True)
class SolverDiagnostics:
    initial_mass: float
    final_mass: float
    initial_energy: float
    final_energy: float
    initial_momentum: tuple[float, float]
    final_momentum: tuple[float, float]
    particle_collision_count: int
    boundary_collision_count: int
    stale_event_count: int = 0

    @property
    def relative_mass_error(self) -> float:
        return abs(self.final_mass - self.initial_mass) / max(abs(self.initial_mass), 1.0e-30)

    @property
    def relative_energy_error(self) -> float:
        return abs(self.final_energy - self.initial_energy) / max(
            abs(self.initial_energy), 1.0e-30
        )

    @property
    def absolute_momentum_error(self) -> float:
        dx = self.final_momentum[0] - self.initial_momentum[0]
        dy = self.final_momentum[1] - self.initial_momentum[1]
        return sqrt(dx * dx + dy * dy)


@dataclass(frozen=True, slots=True)
class SimulationResult:
    backend: str
    event_semantics: Literal[
        "geometric_collision",
        "kinetic_collision",
        "admissible_collision_overlap",
    ]
    snapshots: tuple[Snapshot, ...]
    collision_events: tuple[CollisionEvent, ...]
    diagnostics: SolverDiagnostics
    geometry_collision_events: tuple[GeometryCollisionEvent, ...] = ()

    def __post_init__(self) -> None:
        if not self.backend:
            raise ValueError("backend must not be empty")
        if not self.snapshots:
            raise ValueError("at least one snapshot is required")
        times = [snapshot.time for snapshot in self.snapshots]
        if times != sorted(times):
            raise ValueError("snapshot times must be non-decreasing")
