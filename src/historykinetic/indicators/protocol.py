from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from historykinetic.contracts import BlockStateSummary, HistoryFeatures


class RefinementIndicator(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def runtime_observable_only(self) -> bool: ...

    def score(
        self,
        state: BlockStateSummary,
        history: HistoryFeatures | None,
        context: Mapping[str, float],
    ) -> float: ...
