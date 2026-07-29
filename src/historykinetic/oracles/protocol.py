from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol

from historykinetic.contracts import ArtifactRef


class OracleAdapter(Protocol):
    @property
    def source_id(self) -> str: ...

    @property
    def pinned_revision(self) -> str: ...

    def prepare(self, case: Mapping[str, object], run_directory: Path) -> Path: ...

    def execute(self, prepared_input: Path, run_directory: Path) -> None: ...

    def convert(self, run_directory: Path) -> tuple[ArtifactRef, ...]: ...
