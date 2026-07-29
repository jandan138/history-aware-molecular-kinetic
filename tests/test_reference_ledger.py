from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_software_sources_are_pinned() -> None:
    payload = yaml.safe_load((ROOT / "references" / "sources.yaml").read_text(encoding="utf-8"))
    ids: set[str] = set()
    for source in payload["sources"]:
        assert source["id"] not in ids
        ids.add(source["id"])
        if source["kind"] == "software":
            assert len(source["pinned_revision"]) >= 12
            assert source["integration"] in {"external_process", "reference_only"}
