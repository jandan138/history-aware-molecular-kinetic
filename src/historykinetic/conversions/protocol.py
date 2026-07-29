from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from historykinetic.contracts import ArtifactRef, ConservationBudget, RepresentationKind


@dataclass(frozen=True, slots=True)
class ConversionRequest:
    source: RepresentationKind
    target: RepresentationKind
    block_ids: tuple[str, ...]
    time: float
    policy: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class ConversionResult:
    artifacts: tuple[ArtifactRef, ...]
    conservation: ConservationBudget
    diagnostics: Mapping[str, float]


class RepresentationConverter(Protocol):
    @property
    def name(self) -> str: ...

    def convert(
        self,
        request: ConversionRequest,
        input_artifacts: tuple[ArtifactRef, ...],
        output_directory: Path,
    ) -> ConversionResult: ...
