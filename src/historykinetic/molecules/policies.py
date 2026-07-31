from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Protocol

from historykinetic.molecules.models import (
    EncounterContext,
    EncounterDecision,
    PolicyDecision,
)
from historykinetic.molecules.tracker import MoleculeTracker


class CollisionPolicy(Protocol):
    name: str

    def decide(
        self,
        context: EncounterContext,
        tracker: MoleculeTracker,
    ) -> PolicyDecision: ...


@dataclass(frozen=True, slots=True)
class FullCollisionPolicy:
    name: str = "full"

    def decide(
        self,
        context: EncounterContext,
        tracker: MoleculeTracker,
    ) -> PolicyDecision:
        del context, tracker
        return PolicyDecision(EncounterDecision.ACCEPT, "full-policy")


@dataclass(frozen=True, slots=True)
class GhostCollisionPolicy:
    name: str = "ghost"

    def decide(
        self,
        context: EncounterContext,
        tracker: MoleculeTracker,
    ) -> PolicyDecision:
        del context, tracker
        return PolicyDecision(EncounterDecision.SUPPRESS, "ghost-policy")


@dataclass(frozen=True, slots=True)
class MoleculeBudgetPolicy:
    maximum_component_size: int
    maximum_cycle_rank: int

    @property
    def name(self) -> str:
        return f"budget-l{self.maximum_component_size}-g{self.maximum_cycle_rank}"

    def decide(
        self,
        context: EncounterContext,
        tracker: MoleculeTracker,
    ) -> PolicyDecision:
        allowed, reason = tracker.budget_allows(
            context.particle_a,
            context.particle_b,
            size=self.maximum_component_size,
            cycles=self.maximum_cycle_rank,
        )
        return PolicyDecision(
            EncounterDecision.ACCEPT if allowed else EncounterDecision.SUPPRESS,
            reason,
        )


class QuotaMatchedRandomPolicy:
    """Randomly select a count/time-layer-matched collision dose.

    Within each layer this is sequential sampling without replacement when the
    candidate encounter count matches the structured target. It consults only
    encounter counts, never a scientific response observable.
    """

    name = "count-time-matched-random"

    def __init__(
        self,
        *,
        target_accepted_by_layer: dict[int, int],
        target_encounters_by_layer: dict[int, int],
        seed: int,
    ) -> None:
        self._target_accepted = dict(target_accepted_by_layer)
        self._target_encounters = dict(target_encounters_by_layer)
        self._seen: defaultdict[int, int] = defaultdict(int)
        self._accepted: defaultdict[int, int] = defaultdict(int)
        self._rng = random.Random(seed)

    def decide(
        self,
        context: EncounterContext,
        tracker: MoleculeTracker,
    ) -> PolicyDecision:
        del tracker
        layer = context.layer
        target_accepts = self._target_accepted.get(layer, 0)
        target_encounters = self._target_encounters.get(layer, 0)
        seen = self._seen[layer]
        accepted = self._accepted[layer]
        remaining_accepts = max(0, target_accepts - accepted)
        remaining_slots = max(1, target_encounters - seen)
        self._seen[layer] += 1
        if remaining_accepts == 0:
            return PolicyDecision(EncounterDecision.SUPPRESS, "random-quota-filled")
        probability = min(1.0, remaining_accepts / remaining_slots)
        if self._rng.random() < probability:
            self._accepted[layer] += 1
            return PolicyDecision(EncounterDecision.ACCEPT, "random-quota-selected")
        return PolicyDecision(EncounterDecision.SUPPRESS, "random-quota-rejected")


class TopologyShuffledBudgetPolicy:
    def __init__(
        self,
        *,
        maximum_component_size: int,
        maximum_cycle_rank: int,
        seed: int,
    ) -> None:
        self.maximum_component_size = maximum_component_size
        self.maximum_cycle_rank = maximum_cycle_rank
        self.seed = seed
        self._last_layer: int | None = None

    @property
    def name(self) -> str:
        return (
            f"topology-shuffled-l{self.maximum_component_size}"
            f"-g{self.maximum_cycle_rank}"
        )

    def decide(
        self,
        context: EncounterContext,
        tracker: MoleculeTracker,
    ) -> PolicyDecision:
        if context.layer != self._last_layer:
            tracker.shuffle_membership(seed=self.seed + context.layer)
            self._last_layer = context.layer
        allowed, reason = tracker.budget_allows(
            context.particle_a,
            context.particle_b,
            size=self.maximum_component_size,
            cycles=self.maximum_cycle_rank,
        )
        return PolicyDecision(
            EncounterDecision.ACCEPT if allowed else EncounterDecision.SUPPRESS,
            f"topology-shuffled:{reason}",
        )
