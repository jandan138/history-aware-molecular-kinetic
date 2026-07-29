from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol

from historykinetic.contracts import ArtifactRef


class SolverBackend(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def semantic_version(self) -> str: ...

    def validate_case(self, case: Mapping[str, object]) -> None: ...

    def run(self, case: Mapping[str, object], run_directory: Path) -> tuple[ArtifactRef, ...]: ...
