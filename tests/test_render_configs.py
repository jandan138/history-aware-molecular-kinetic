from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml

from historykinetic.rendering import RenderPurpose, render_summary_from_mapping

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_render_configs_validate_and_build_semantic_summaries() -> None:
    schema = _load_json(ROOT / "schemas" / "render-config.schema.json")
    validator = jsonschema.Draft202012Validator(schema)
    config_paths = sorted((ROOT / "configs" / "render").glob("*.yml"))
    assert config_paths

    summaries = []
    for path in config_paths:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        validator.validate(payload)
        summaries.append(render_summary_from_mapping(payload))

    assert {summary.purpose for summary in summaries} == {
        RenderPurpose.DIAGNOSTIC,
        RenderPurpose.SHARED_COMPARISON,
        RenderPurpose.HERO,
    }
    assert len({summary.stable_id for summary in summaries}) == len(summaries)


def test_primary_configs_have_complete_comparison_locks() -> None:
    for path in sorted((ROOT / "configs" / "render").glob("*.yml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        summary = render_summary_from_mapping(payload)
        if summary.purpose is RenderPurpose.DIAGNOSTIC:
            assert not summary.comparison_lock.enabled
        else:
            assert summary.comparison_lock.is_primary_ready


def test_render_manifest_example_validates() -> None:
    schema = _load_json(ROOT / "schemas" / "render-manifest.schema.json")
    example = _load_json(ROOT / "schemas" / "examples" / "render-manifest.json")
    jsonschema.Draft202012Validator(schema).validate(example)
