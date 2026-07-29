from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_json_schemas_are_valid_draft_2020_12() -> None:
    schemas = sorted((ROOT / "schemas").glob("*.schema.json"))
    assert schemas, "expected at least one JSON schema"
    for path in schemas:
        jsonschema.Draft202012Validator.check_schema(_load(path))
