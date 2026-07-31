from __future__ import annotations

from dataclasses import dataclass

from historykinetic.echo.models import PassiveColorMap
from historykinetic.solvers import SimulationResult
from historykinetic.timeline import (
    CausalBranchResult,
    CausalCheckpoint,
    CausalEvent,
    TimelineRun,
)

from .protocol import MolecularTimeMachineE3Protocol


@dataclass(frozen=True, slots=True)
class E3Metrics:
    baseline_terminal_color_score: float
    edited_terminal_color_score: float
    terminal_color_gap: float
    visibly_changed_particle_count: int
    visibly_changed_particle_fraction: float
    baseline_graph_descendant_particle_count: int
    baseline_graph_descendant_particle_fraction: float


@dataclass(frozen=True, slots=True)
class MolecularTimeMachineE3Result:
    protocol: MolecularTimeMachineE3Protocol
    colors: PassiveColorMap
    preparation: SimulationResult
    timeline: TimelineRun
    target_event: CausalEvent
    fork_checkpoint: CausalCheckpoint
    branch: CausalBranchResult
    metrics: E3Metrics

