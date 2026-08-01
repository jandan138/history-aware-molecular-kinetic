"""Typed results for the E4 causal-steering Hero."""

from __future__ import annotations

from dataclasses import dataclass

from historykinetic.echo.models import PassiveColorMap
from historykinetic.solvers import SimulationResult
from historykinetic.timeline import (
    CausalBranchPreview,
    CausalBranchResult,
    CausalCheckpoint,
    CausalEvent,
    TimelineRun,
)

from .protocol import MolecularTimeMachineE4Protocol


@dataclass(frozen=True, slots=True)
class CausalTarget:
    """A creator-selected terminal feature and its exact particle membership."""

    target_id: str
    description: str
    x_bounds: tuple[float, float]
    y_bounds: tuple[float, float]
    particle_ids: tuple[int, ...]
    collateral_foreground_particle_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CausalCandidate:
    """One historical collision ranked from baseline ancestry only."""

    rank: int
    event: CausalEvent
    descendant_particle_ids: tuple[int, ...]
    target_descendant_particle_ids: tuple[int, ...]
    coverage: float
    purity: float
    causal_score: float


@dataclass(frozen=True, slots=True)
class TargetChangeMetrics:
    """Outcome readout for the one selected visual target."""

    target_ejection_fraction: float
    collateral_ejection_fraction: float
    target_to_collateral_ratio: float
    target_ejected_particle_ids: tuple[int, ...]
    collateral_ejected_particle_ids: tuple[int, ...]

    @property
    def steering_score(self) -> float:
        """Registered utility used only to choose an angle in the small palette."""

        return self.target_ejection_fraction - self.collateral_ejection_fraction


@dataclass(frozen=True, slots=True)
class PalettePreview:
    """One cached, exact local preview for a collision/angle choice."""

    candidate: CausalCandidate
    angle_degrees: float
    preview: CausalBranchPreview
    target_metrics: TargetChangeMetrics


@dataclass(frozen=True, slots=True)
class E4Metrics:
    baseline_terminal_color_score: float
    selected_candidate_rank: int
    selected_candidate_causal_score: float
    selected_angle_degrees: float
    preview_count: int
    preview_median_seconds: float
    target_particle_count: int
    collateral_foreground_particle_count: int
    target_ejection_fraction: float
    collateral_ejection_fraction: float
    target_to_collateral_ratio: float
    selected_branch_reuse_fraction: float
    selected_branch_peak_affected_fraction: float


@dataclass(frozen=True, slots=True)
class MolecularTimeMachineE4Result:
    protocol: MolecularTimeMachineE4Protocol
    colors: PassiveColorMap
    preparation: SimulationResult
    timeline: TimelineRun
    target: CausalTarget
    candidates: tuple[CausalCandidate, ...]
    palette: tuple[PalettePreview, ...]
    selected_preview: PalettePreview
    selected_checkpoint: CausalCheckpoint
    selected_branch: CausalBranchResult
    metrics: E4Metrics
