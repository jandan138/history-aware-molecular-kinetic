from __future__ import annotations

from dataclasses import dataclass

from historykinetic.echo.protocol import EchoBranchKind, EchoE1Protocol
from historykinetic.solvers import DiskState, SimulationResult


@dataclass(frozen=True, slots=True)
class PassiveColorMap:
    labels_by_particle_id: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.labels_by_particle_id:
            raise ValueError("passive color map must not be empty")
        if not set(self.labels_by_particle_id).issubset({0, 1}):
            raise ValueError("E1 passive colors must be binary")
        if 0 not in self.labels_by_particle_id or 1 not in self.labels_by_particle_id:
            raise ValueError("E1 passive colors must contain foreground and background")

    def label(self, particle_id: int) -> int:
        if not 0 <= particle_id < len(self.labels_by_particle_id):
            raise KeyError(f"particle ID is outside the passive color map: {particle_id}")
        return self.labels_by_particle_id[particle_id]


@dataclass(frozen=True, slots=True)
class BranchRun:
    kind: EchoBranchKind
    result: SimulationResult


@dataclass(frozen=True, slots=True)
class ReversalAudit:
    particle_count: int
    seed: int
    forward_event_count: int
    reverse_event_count: int
    event_pair_agreement: float
    maximum_mirrored_event_time_error: float
    position_rms: float
    velocity_rms: float
    relative_energy_error: float
    absolute_momentum_error: float


@dataclass(frozen=True, slots=True)
class ResolvedStateAudit:
    particle_count: int
    seed: int
    blocks_x: int
    blocks_y: int
    velocity_bin_count: int
    total_variation: float
    maximum_count_fraction_mismatch: float
    maximum_momentum_mismatch: float
    maximum_energy_mismatch: float
    maximum_anisotropy_mismatch: float


@dataclass(frozen=True, slots=True)
class EchoMetricRow:
    particle_count: int
    seed: int
    branch: EchoBranchKind
    time: float
    color_score: float
    color_recovery: float
    anisotropy: float


@dataclass(frozen=True, slots=True)
class EchoCaseResult:
    particle_count: int
    seed: int
    initial_state: DiskState
    colors: PassiveColorMap
    preparation: SimulationResult
    pivot_reverse_state: DiskState
    branches: tuple[BranchRun, ...]
    reversal_audit: ReversalAudit
    resolved_state_audits: tuple[ResolvedStateAudit, ...]
    changed_particle_fraction: float
    invariant_mismatch: float
    metrics: tuple[EchoMetricRow, ...]

    def branch(self, kind: EchoBranchKind) -> BranchRun:
        for branch in self.branches:
            if branch.kind is kind:
                return branch
        raise KeyError(f"missing E1 branch: {kind.value}")


@dataclass(frozen=True, slots=True)
class EchoStudyResult:
    protocol: EchoE1Protocol
    cases: tuple[EchoCaseResult, ...]
