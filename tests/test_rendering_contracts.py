from __future__ import annotations

from pathlib import PurePosixPath

import pytest

from historykinetic.rendering import (
    PRIMARY_COMPARISON_LOCK_FIELDS,
    ComparisonLock,
    RenderArtifactInput,
    RenderChannel,
    RenderConfigSummary,
    RenderPurpose,
)


def test_primary_render_summary_requires_complete_comparison_lock() -> None:
    lock = ComparisonLock(
        enabled=True,
        group_id="primary-v0",
        locked_fields=tuple(sorted(PRIMARY_COMPARISON_LOCK_FIELDS)),
    )
    summary = RenderConfigSummary(
        config_id="RENDER-SHARED-COMPARISON-v0",
        purpose=RenderPurpose.SHARED_COMPARISON,
        camera_path_id="camera-v0",
        channels=(RenderChannel.EXACT_PARTICLES, RenderChannel.DENSITY_VOLUME),
        comparison_lock=lock,
        statistical_non_physical_label=True,
        future_frame_access=False,
    )
    assert summary.comparison_lock.is_primary_ready
    assert summary.stable_id.startswith("render-config-")


def test_primary_render_summary_rejects_incomplete_lock() -> None:
    lock = ComparisonLock(enabled=True, group_id="primary-v0", locked_fields=("camera",))
    with pytest.raises(ValueError, match="complete comparison lock"):
        RenderConfigSummary(
            config_id="RENDER-SHARED-COMPARISON-v0",
            purpose=RenderPurpose.SHARED_COMPARISON,
            camera_path_id="camera-v0",
            channels=(RenderChannel.EXACT_PARTICLES,),
            comparison_lock=lock,
            statistical_non_physical_label=True,
            future_frame_access=False,
        )


def test_render_artifact_input_requires_relative_path_and_digest() -> None:
    artifact = RenderArtifactInput(
        kind="particle_bundle",
        path=PurePosixPath("artifacts/particles.json"),
        schema_version="1.0.0",
        sha256="a" * 64,
    )
    assert artifact.path.as_posix() == "artifacts/particles.json"

    with pytest.raises(ValueError, match="relative"):
        RenderArtifactInput(
            kind="particle_bundle",
            path=PurePosixPath("/tmp/particles.json"),
            schema_version="1.0.0",
            sha256="a" * 64,
        )
