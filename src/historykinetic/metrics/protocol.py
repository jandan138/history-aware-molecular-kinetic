from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

from historykinetic.contracts import ArtifactRef


class Metric(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def units(self) -> str: ...

    def evaluate(self, artifacts: Sequence[ArtifactRef]) -> Mapping[str, float]: ...
