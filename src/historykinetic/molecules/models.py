from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from historykinetic.solvers.result import SimulationResult


class EncounterDecision(StrEnum):
    ACCEPT = "accepted_collision"
    SUPPRESS = "suppressed_overlap"


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    decision: EncounterDecision
    reason: str

    def __post_init__(self) -> None:
        if not self.reason:
            raise ValueError("policy decision reason must not be empty")


@dataclass(frozen=True, slots=True)
class ComponentView:
    component_id: int
    size: int
    cycle_rank: int


@dataclass(frozen=True, slots=True)
class EncounterContext:
    time: float
    layer: int
    particle_a: int
    particle_b: int
    encounter_index: int


@dataclass(frozen=True, slots=True)
class EncounterEvent:
    event_id: int
    time: float
    layer: int
    particle_a: int
    particle_b: int
    block_id: str
    contact_normal: tuple[float, float]
    incoming_relative_normal_velocity: float
    pre_velocity_a: tuple[float, float]
    pre_velocity_b: tuple[float, float]
    post_velocity_a: tuple[float, float]
    post_velocity_b: tuple[float, float]
    decision: EncounterDecision
    reason: str
    predecessor_event_a: int | None
    predecessor_event_b: int | None
    component_a_before: int
    component_b_before: int
    component_a_size_before: int
    component_b_size_before: int
    component_a_cycle_rank_before: int
    component_b_cycle_rank_before: int
    component_after: int | None
    component_size_after: int | None
    component_cycle_rank_after: int | None
    pair_multiplicity: int

    @property
    def ordered_pair(self) -> tuple[int, int]:
        return (
            min(self.particle_a, self.particle_b),
            max(self.particle_a, self.particle_b),
        )


@dataclass(frozen=True, slots=True)
class OverlapExitEvent:
    time: float
    particle_a: int
    particle_b: int


@dataclass(frozen=True, slots=True)
class ModifiedSimulationResult:
    policy_name: str
    layer_width: float
    simulation: SimulationResult
    encounter_events: tuple[EncounterEvent, ...]
    overlap_exit_events: tuple[OverlapExitEvent, ...]
    maximum_simultaneous_overlaps: int

    def __post_init__(self) -> None:
        if not self.policy_name:
            raise ValueError("modified result requires a policy name")
        if self.layer_width <= 0:
            raise ValueError("modified result layer width must be positive")

    @property
    def accepted_encounters(self) -> tuple[EncounterEvent, ...]:
        return tuple(
            event
            for event in self.encounter_events
            if event.decision is EncounterDecision.ACCEPT
        )

    @property
    def suppressed_encounters(self) -> tuple[EncounterEvent, ...]:
        return tuple(
            event
            for event in self.encounter_events
            if event.decision is EncounterDecision.SUPPRESS
        )
