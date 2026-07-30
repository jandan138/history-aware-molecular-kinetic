from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Protocol

from historykinetic.contracts import ArtifactRef


class Renderer(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def version(self) -> str: ...

    def render(
        self,
        artifacts: Sequence[ArtifactRef],
        render_config: Mapping[str, object],
        output_directory: Path,
        *,
        evidence_links: Mapping[str, object] | None = None,
    ) -> tuple[Path, ...]: ...
