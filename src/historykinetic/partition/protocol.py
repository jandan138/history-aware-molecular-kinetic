from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from historykinetic.contracts import PartitionDecision, RepresentationKind


class PartitionController(Protocol):
    @property
    def promote_threshold(self) -> float: ...

    @property
    def demote_threshold(self) -> float: ...

    def decide(
        self,
        block_id: str,
        time: float,
        current: RepresentationKind,
        features: Mapping[str, float],
    ) -> PartitionDecision: ...
