from __future__ import annotations

import copy
from pathlib import PurePosixPath

import yaml

from historykinetic.contracts import ArtifactRef
from historykinetic.rendering import RenderPlan, audit_manifests, build_render_manifest


def _config() -> dict[str, object]:
    with open("configs/render/shared-comparison.yml", encoding="utf-8") as stream:
        payload = yaml.safe_load(stream)
    assert isinstance(payload, dict)
    return payload


def _manifest(digest: str, run_id: str) -> dict[str, object]:
    plan = RenderPlan.from_mapping(_config())
    artifact = ArtifactRef(
        "metrics-report",
        PurePosixPath(f"runs/{run_id}/metrics.json"),
        "1.0.0",
        digest * 64,
    )
    return build_render_manifest(
        plan,
        [artifact],
        renderer_name="shared-test-renderer",
        renderer_version="1.0.0",
        evidence_links={
            "case_id": "B5-SHARED-COMPARISON-v0",
            "run_ids": [run_id],
            "claim_ids": ["C7"],
        },
    )


def test_matching_manifests_pass_comparison_audit() -> None:
    first = _manifest("a", "run-reference")
    second = _manifest("b", "run-proposed")
    assert audit_manifests([first, second], require_complete_evidence=True) == []


def test_camera_or_lock_mismatch_fails_comparison_audit() -> None:
    first = _manifest("a", "run-reference")
    second = copy.deepcopy(_manifest("b", "run-proposed"))
    config = second["config"]
    assert isinstance(config, dict)
    config["comparison_lock_digest"] = "comparison-lock-0000000000000000"
    errors = audit_manifests([first, second])
    assert any("comparison-lock digests differ" in error for error in errors)


def test_display_policy_digest_mismatch_fails_comparison_audit() -> None:
    first = _manifest("a", "run-reference")
    second = copy.deepcopy(_manifest("b", "run-proposed"))
    config = second["config"]
    assert isinstance(config, dict)
    config["display_policy_digest"] = "display-policy-0000000000000000"
    errors = audit_manifests([first, second])
    assert any("display-policy digests differ" in error for error in errors)
