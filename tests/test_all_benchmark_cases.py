from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_all_candidate_and_frozen_cases_validate() -> None:
    schema = json.loads((ROOT / "schemas/benchmark-case.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for path in sorted((ROOT / "benchmarks").glob("*/cases/**/*.yml")):
        validator.validate(yaml.safe_load(path.read_text(encoding="utf-8")))


def test_partition_example_validates() -> None:
    schema = json.loads((ROOT / "schemas/partition-mask.schema.json").read_text(encoding="utf-8"))
    example_path = ROOT / "schemas/examples/partition-mask.json"
    example = json.loads(example_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(example)
