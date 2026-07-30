"""A dependency-free renderer boundary implementation.

It deliberately renders no pixels.  It writes a deterministic manifest so the
artifact/config/provenance contract can be exercised before a GPU renderer is
selected.  Production renderers should implement the same protocol and include
the manifest beside their image sequence.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from historykinetic.contracts import ArtifactRef
from historykinetic.rendering.contracts import RenderPlan, build_render_manifest, write_manifest


class ManifestOnlyRenderer:
    @property
    def name(self) -> str:
        return "manifest-only"

    @property
    def version(self) -> str:
        return "0.1.0"

    def render(
        self,
        artifacts: Sequence[ArtifactRef],
        render_config: Mapping[str, object],
        output_directory: Path,
        *,
        evidence_links: Mapping[str, object] | None = None,
    ) -> tuple[Path, ...]:
        plan = RenderPlan.from_mapping(render_config)
        manifest = build_render_manifest(
            plan,
            artifacts,
            renderer_name=self.name,
            renderer_version=self.version,
            evidence_links=evidence_links,
        )
        output = write_manifest(output_directory / "render-manifest.json", manifest)
        return (output,)
