"""Dependency-free semantic contracts shared by solvers and adapters.

These types describe meaning and provenance, not high-performance array layouts.
Large particle and grid arrays live in versioned external artifacts.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from math import sqrt
from pathlib import PurePosixPath


class BenchmarkSuite(StrEnum):
    R0 = "R0"
    B0 = "B0"
    B1 = "B1"
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"
    B5 = "B5"


class RepresentationKind(StrEnum):
    EXACT_HARD_SPHERE = "exact_hard_sphere"
    BOLTZMANN_DSMC = "boltzmann_dsmc"
    ENSKOG_PARTICLE = "enskog_particle"
    SHADOW_EDMD_PROBE = "shadow_edmd_probe"
    UNRESOLVED = "unresolved"


class RunStatus(StrEnum):
    RUNNING = "running"
    PASSED = "passed"
    FAILED_METRIC = "failed_metric"
    NUMERICAL_INSTABILITY = "numerical_instability"
    ADAPTER_FAILURE = "adapter_failure"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    INVALID_INPUT = "invalid_input"
    LICENSE_BLOCKED = "license_blocked"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    kind: str
    path: PurePosixPath
    schema_version: str
    content_sha256: str | None = None

    def __post_init__(self) -> None:
        if self.path.is_absolute():
            raise ValueError("artifact paths must be repository/run-relative")
        if not self.kind:
            raise ValueError("artifact kind must not be empty")
        if not self.schema_version:
            raise ValueError("schema version must not be empty")


@dataclass(frozen=True, slots=True)
class CollisionEvent:
    time: float
    particle_a: int
    particle_b: int
    block_id: str
    pre_velocity_a: tuple[float, float, float]
    pre_velocity_b: tuple[float, float, float]
    post_velocity_a: tuple[float, float, float]
    post_velocity_b: tuple[float, float, float]
    contact_normal: tuple[float, float] | None = None
    incoming_relative_normal_velocity: float | None = None

    def __post_init__(self) -> None:
        if self.time < 0:
            raise ValueError("collision time must be non-negative")
        if self.particle_a < 0 or self.particle_b < 0:
            raise ValueError("particle IDs must be non-negative")
        if self.particle_a == self.particle_b:
            raise ValueError("a particle cannot collide with itself")
        if not self.block_id:
            raise ValueError("block_id must not be empty")
        if self.contact_normal is not None and len(self.contact_normal) != 2:
            raise ValueError("contact_normal must contain two components")

    @property
    def ordered_pair(self) -> tuple[int, int]:
        return (
            min(self.particle_a, self.particle_b),
            max(self.particle_a, self.particle_b),
        )


@dataclass(frozen=True, slots=True)
class BlockStateSummary:
    block_id: str
    time: float
    density: float
    packing_fraction: float
    mean_velocity: tuple[float, float, float]
    temperature: float
    knudsen_gll: float
    maxwellian_residual: float
    stress_deviator_norm: float
    heat_flux_norm: float
    sample_count: int

    def __post_init__(self) -> None:
        if self.time < 0:
            raise ValueError("time must be non-negative")
        for name in (
            "density",
            "packing_fraction",
            "temperature",
            "knudsen_gll",
            "maxwellian_residual",
            "stress_deviator_norm",
            "heat_flux_norm",
        ):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be non-negative")
        if not 0 <= self.packing_fraction < 1:
            raise ValueError("packing_fraction must lie in [0, 1)")
        if self.sample_count < 0:
            raise ValueError("sample_count must be non-negative")


@dataclass(frozen=True, slots=True)
class HistoryFeatures:
    window_start: float
    window_end: float
    collision_count: int
    unique_pair_count: int
    repeated_pair_ratio: float
    vertex_count: int
    component_count: int
    cycle_rank: int
    largest_component_fraction: float
    mean_lineage_depth: float
    c2_proxy_norm: float

    def __post_init__(self) -> None:
        if self.window_start < 0 or self.window_end < self.window_start:
            raise ValueError("invalid history window")
        for name in (
            "collision_count",
            "unique_pair_count",
            "vertex_count",
            "component_count",
            "cycle_rank",
        ):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be non-negative")
        for name in ("repeated_pair_ratio", "largest_component_fraction"):
            value = getattr(self, name)
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must lie in [0, 1]")
        if self.mean_lineage_depth < 0 or self.c2_proxy_norm < 0:
            raise ValueError("history norms must be non-negative")


@dataclass(frozen=True, slots=True)
class ConservationBudget:
    mass_before: float
    mass_after: float
    momentum_before: tuple[float, float, float]
    momentum_after: tuple[float, float, float]
    energy_before: float
    energy_after: float

    def _relative(self, before: float, after: float) -> float:
        scale = max(abs(before), 1.0e-30)
        return abs(after - before) / scale

    @property
    def relative_mass_error(self) -> float:
        return self._relative(self.mass_before, self.mass_after)

    @property
    def relative_energy_error(self) -> float:
        return self._relative(self.energy_before, self.energy_after)

    @property
    def absolute_momentum_error(self) -> float:
        delta = tuple(a - b for a, b in zip(self.momentum_after, self.momentum_before, strict=True))
        return sqrt(sum(component * component for component in delta))


@dataclass(frozen=True, slots=True)
class PartitionDecision:
    block_id: str
    time: float
    current: RepresentationKind
    target: RepresentationKind
    score: float
    threshold: float
    reason: str
    observable_features: Mapping[str, float]
    oracle_only_features: Mapping[str, float]

    def __post_init__(self) -> None:
        if self.time < 0:
            raise ValueError("time must be non-negative")
        if not self.reason:
            raise ValueError("reason must not be empty")
