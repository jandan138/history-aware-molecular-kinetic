from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_external_source_locks_validate() -> None:
    schema = _load_json(ROOT / "schemas" / "source-lock.schema.json")
    validator = jsonschema.Draft202012Validator(schema)
    locks = sorted((ROOT / "adapters").glob("*/source.lock.yml"))
    assert locks, "expected at least one external source lock"
    for path in locks:
        validator.validate(yaml.safe_load(path.read_text(encoding="utf-8")))


def test_source_locks_match_reference_ledger() -> None:
    ledger = yaml.safe_load((ROOT / "references" / "sources.yaml").read_text(encoding="utf-8"))
    software = {
        source["id"]: source
        for source in ledger["sources"]
        if source["kind"] == "software"
    }
    for path in sorted((ROOT / "adapters").glob("*/source.lock.yml")):
        lock = yaml.safe_load(path.read_text(encoding="utf-8"))
        source = software[lock["source_id"]]
        assert lock["repository"] == source["repository"]
        assert lock["revision"] == source["pinned_revision"]
        assert lock["integration"] == source["integration"]
