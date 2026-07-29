from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_json_examples_validate() -> None:
    pairs = [
        ("schemas/collision-event.schema.json", "schemas/examples/collision-event.json"),
        ("schemas/history-feature.schema.json", "schemas/examples/history-feature.json"),
    ]
    for schema_path, example_path in pairs:
        jsonschema.Draft202012Validator(load_json(schema_path)).validate(load_json(example_path))


def test_benchmark_yaml_examples_validate() -> None:
    schema = load_json("schemas/benchmark-case.schema.json")
    validator = jsonschema.Draft202012Validator(schema)
    for path in sorted((ROOT / "configs" / "examples").glob("*.yml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        validator.validate(payload)
