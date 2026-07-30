from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_all_candidate_and_frozen_benchmark_cases_validate() -> None:
    schema = _load_json("schemas/benchmark-case.schema.json")
    validator = jsonschema.Draft202012Validator(schema)
    paths = sorted((ROOT / "benchmarks").glob("*/cases/**/*.yml"))
    assert paths
    for path in paths:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        validator.validate(payload)


def test_b5_visual_cases_bind_existing_scene_configs_and_claims() -> None:
    case_root = ROOT / "benchmarks/b5_graphics_evidence/cases/candidate"
    for path in sorted(case_root.glob("B5-*.yml")):
        case = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(case, dict)
        physics = case["physics"]
        assert isinstance(physics, dict)
        render_config_path = ROOT / str(physics["render_config"])
        assert render_config_path.exists()
        claims = physics["primary_claims"]
        assert isinstance(claims, list) and claims

        render_config = yaml.safe_load(render_config_path.read_text(encoding="utf-8"))
        assert render_config["scene_id"] == case["case_id"]
