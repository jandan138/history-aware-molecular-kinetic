"""Typed results for the E5 Same Present, Chosen Future Hero."""

from __future__ import annotations

from dataclasses import dataclass

from historykinetic.echo.models import PassiveColorMap
from historykinetic.solvers import DiskState, SimulationResult

from .protocol import MolecularTimeMachineE5Protocol


@dataclass(frozen=True, slots=True)
class FutureTarget:
    target_id: str
    description: str
    x_bounds: tuple[float, float]
    y_bounds: tuple[float, float]
    particle_ids: tuple[int, ...]
    collateral_foreground_particle_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class VelocityOwnershipSurgery:
    pivot_time: float
    declared_spatial_grid: tuple[int, int]
    swaps: tuple[tuple[int, int], ...]

    @property
    def touched_particle_ids(self) -> tuple[int, ...]:
        return tuple(sorted(particle_id for pair in self.swaps for particle_id in pair))

    @property
    def surgery_id(self) -> str:
        pairs = "__".join(f"{left}-{right}" for left, right in self.swaps)
        return f"velocity-ownership-{pairs}"


@dataclass(frozen=True, slots=True)
class ResolvedPresentAudit:
    positions_identical: bool
    colors_identical: bool
    particle_arrays_identical_except_velocity_ownership: bool
    declared_cell_velocity_multisets_identical: bool
    declared_cell_target_velocity_multisets_identical: bool
    geometry_valid: bool
    mass_error: float
    momentum_error: float
    energy_error: float


@dataclass(frozen=True, slots=True)
class FutureOutcomeMetrics:
    target_particle_count: int
    baseline_target_region_occupancy: int
    edited_target_region_occupancy: int
    target_ejected_particle_ids: tuple[int, ...]
    target_ejection_fraction: float
    target_region_reduction_fraction: float
    collateral_particle_count: int
    collateral_retained_particle_ids: tuple[int, ...]
    collateral_retention_fraction: float
    edited_foreground_inside_pattern_count: int


@dataclass(frozen=True, slots=True)
class SurgeryPreview:
    surgery: VelocityOwnershipSurgery
    edited_pivot: DiskState
    audit: ResolvedPresentAudit
    simulation: SimulationResult
    outcome: FutureOutcomeMetrics
    wall_seconds: float


@dataclass(frozen=True, slots=True)
class PivotReplayAudit:
    terminal_position_rms: float
    terminal_velocity_rms: float
    collision_pair_agreement: float


@dataclass(frozen=True, slots=True)
class E5Metrics:
    preview_count: int
    preview_median_seconds: float
    selected_swap_count: int
    touched_particle_count: int
    touched_particle_fraction: float
    target_ejection_fraction: float
    target_region_reduction_fraction: float
    collateral_retention_fraction: float


@dataclass(frozen=True, slots=True)
class MolecularTimeMachineE5Result:
    protocol: MolecularTimeMachineE5Protocol
    colors: PassiveColorMap
    preparation: SimulationResult
    baseline: SimulationResult
    pivot_state: DiskState
    pivot_replay: SimulationResult
    pivot_replay_audit: PivotReplayAudit
    target: FutureTarget
    previews: tuple[SurgeryPreview, ...]
    selected_preview: SurgeryPreview
    metrics: E5Metrics
