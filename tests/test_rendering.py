from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath

import jsonschema
import pytest
import yaml

from historykinetic.contracts import ArtifactRef
from historykinetic.rendering import (
    FrameSchedule,
    ManifestOnlyRenderer,
    RenderPlan,
    build_render_manifest,
    comparison_lock_digest,
)

ROOT = Path(__file__).resolve().parents[1]


def _load_yaml(relative: str) -> dict[str, object]:
    payload = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_all_render_configs_validate() -> None:
    schema = json.loads((ROOT / "schemas/render-config.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for path in sorted((ROOT / "configs/render").rglob("*.yml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        validator.validate(payload)


def test_all_camera_paths_validate_and_are_referenced() -> None:
    schema = json.loads((ROOT / "schemas/camera-path.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    camera_root = ROOT / "configs/render/cameras"
    camera_paths = sorted(camera_root.rglob("*.json"))
    assert camera_paths
    for path in camera_paths:
        validator.validate(json.loads(path.read_text(encoding="utf-8")))

    for config_path in sorted((ROOT / "configs/render").rglob("*.yml")):
        payload = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        for camera_path in payload["camera"]["paths"]:
            referenced = ROOT / "configs/render" / camera_path["path_ref"]
            assert referenced.exists(), f"missing camera path: {camera_path['path_ref']}"
            assert hashlib.sha256(referenced.read_bytes()).hexdigest() == camera_path["sha256"]


def test_render_schema_examples_validate() -> None:
    pairs = [
        ("schemas/render-config.schema.json", "schemas/examples/render-config.json"),
        ("schemas/render-manifest.schema.json", "schemas/examples/render-manifest.json"),
    ]
    for schema_path, example_path in pairs:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        example = json.loads((ROOT / example_path).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(example)


def test_complete_render_manifest_requires_case_run_claim_and_metric_links() -> None:
    schema = json.loads((ROOT / "schemas/render-manifest.schema.json").read_text(encoding="utf-8"))
    example = json.loads(
        (ROOT / "schemas/examples/render-manifest.json").read_text(encoding="utf-8")
    )
    example["evidence_links"]["complete"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(example)


def test_frame_schedule_includes_end_point() -> None:
    assert FrameSchedule(0.0, 1.0, 0.1).frame_count == 11


def test_camera_physics_decoupling_is_required() -> None:
    config = _load_yaml("configs/render/diagnostic.yml")
    display_policy = config["display_policy"]
    assert isinstance(display_policy, dict)
    display_policy["physics_camera_decoupled"] = False
    with pytest.raises(ValueError):
        RenderPlan.from_mapping(config)


def test_manifest_only_renderer_is_deterministic(tmp_path: Path) -> None:
    config = _load_yaml("configs/render/shared-comparison.yml")
    artifacts = [
        ArtifactRef(
            "particle-bundle",
            PurePosixPath("artifacts/particles.json"),
            "1.0.0",
            "a" * 64,
        ),
        ArtifactRef(
            "metrics-report",
            PurePosixPath("artifacts/metrics.json"),
            "1.0.0",
            "b" * 64,
        ),
    ]
    renderer = ManifestOnlyRenderer()
    first = renderer.render(artifacts, config, tmp_path / "a")[0]
    second = renderer.render(list(reversed(artifacts)), config, tmp_path / "b")[0]
    assert first.read_text(encoding="utf-8") == second.read_text(encoding="utf-8")

    manifest = json.loads(first.read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/render-manifest.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(manifest)
    assert manifest["evidence"]["all_artifacts_hashed"] is True
    assert manifest["renderer"]["digest"].startswith("renderer-")
    expected_camera_paths = [
        {"path_ref": row["path_ref"], "sha256": row["sha256"]}
        for row in config["camera"]["paths"]
    ]
    assert manifest["camera"]["paths"] == expected_camera_paths
    assert manifest["evidence_links"]["complete"] is False
    assert manifest["evidence_links"]["metric_artifact_paths"] == [
        "artifacts/metrics.json"
    ]


def test_final_evidence_links_can_be_completed_without_changing_render_config() -> None:
    config = _load_yaml("configs/render/scenes/expansion-into-vacuum.yml")
    plan = RenderPlan.from_mapping(config)
    artifacts = [
        ArtifactRef(
            "metrics-report",
            PurePosixPath("runs/run-expansion-v0/metrics.json"),
            "1.0.0",
            "c" * 64,
        )
    ]
    manifest = build_render_manifest(
        plan,
        artifacts,
        renderer_name="test-renderer",
        renderer_version="1.0.0",
        evidence_links={
            "case_id": "B5-EXPANSION-VACUUM-v0",
            "run_ids": ["run-expansion-reference", "run-expansion-proposed"],
            "claim_ids": ["C4", "C7", "C8", "C9"],
        },
    )
    assert manifest["evidence_links"]["complete"] is True
    assert manifest["evidence_links"]["shot_ids"] == list(plan.camera_shot_ids)


def test_comparison_lock_changes_when_locked_camera_changes() -> None:
    config = _load_yaml("configs/render/shared-comparison.yml")
    first = comparison_lock_digest(config)
    camera = config["camera"]
    assert isinstance(camera, dict)
    camera["fov_degrees"] = 43.0
    assert comparison_lock_digest(config) != first
