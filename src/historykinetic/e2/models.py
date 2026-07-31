from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from historykinetic.e2.protocol import MolecularEchoesE2Protocol
from historykinetic.echo.models import PassiveColorMap
from historykinetic.molecules.models import ModifiedSimulationResult
from historykinetic.solvers import DiskState, SimulationResult


class E2Direction(StrEnum):
    FORWARD = "forward"
    REVERSE = "reverse"


@dataclass(frozen=True, slots=True)
class E2BranchRun:
    direction: E2Direction
    name: str
    result: ModifiedSimulationResult


@dataclass(frozen=True, slots=True)
class E2MetricRow:
    particle_count: int
    seed: int
    direction: E2Direction
    branch: str
    time: float
    color_score: float
    color_recovery: float


@dataclass(frozen=True, slots=True)
class E2BranchAudit:
    particle_count: int
    seed: int
    direction: E2Direction
    branch: str
    encounter_count: int
    accepted_collision_count: int
    suppressed_overlap_count: int
    collision_dose: float
    incoming_pair_closure_defect: float
    mirrored_pair_alignment: float
    maximum_simultaneous_overlaps: int
    accepted_by_layer: tuple[tuple[int, int], ...]
    encounters_by_layer: tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class E2CaseResult:
    particle_count: int
    seed: int
    initial_state: DiskState
    colors: PassiveColorMap
    preparation: SimulationResult
    pivot_score: float
    branches: tuple[E2BranchRun, ...]
    metrics: tuple[E2MetricRow, ...]
    audits: tuple[E2BranchAudit, ...]

    def branch(self, direction: E2Direction, name: str) -> E2BranchRun:
        for branch in self.branches:
            if branch.direction is direction and branch.name == name:
                return branch
        raise KeyError(f"missing E2 branch: {direction.value}/{name}")


@dataclass(frozen=True, slots=True)
class E2StudyResult:
    protocol: MolecularEchoesE2Protocol
    cases: tuple[E2CaseResult, ...]


@dataclass(frozen=True, slots=True)
class CalibrationDoseRow:
    seed: int
    direction: E2Direction
    branch: str
    accepted_collision_count: int
    full_collision_count: int
    collision_dose: float


@dataclass(frozen=True, slots=True)
class E2CalibrationResult:
    protocol: MolecularEchoesE2Protocol
    rows: tuple[CalibrationDoseRow, ...]
    selected_branch: str
