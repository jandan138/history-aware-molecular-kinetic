from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
from typing import Any

import jsonschema
import yaml

from historykinetic.contracts import ArtifactRef
from historykinetic.rendering import ManifestOnlyRenderer

ROOT = Path(__file__).resolve().parents[1]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create and validate a deterministic render manifest without rendering pixels."
    )
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--artifacts",
        type=Path,
        required=True,
        help="JSON array with kind, path, schema_version, and content_sha256 fields.",
    )
    parser.add_argument(
        "--case-id",
        help="Frozen/candidate benchmark case linked to this render evidence.",
    )
    parser.add_argument(
        "--run-id",
        action="append",
        default=[],
        help="Run identifier used by this render. Repeat for comparisons.",
    )
    parser.add_argument(
        "--claim-id",
        action="append",
        default=[],
        help="Claim identifier supported by this render (for example C4).",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    args = _parser().parse_args()
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("render config must be a YAML object")

    config_schema = _load_json(ROOT / "schemas/render-config.schema.json")
    jsonschema.Draft202012Validator(config_schema).validate(config)

    rows = _load_json(args.artifacts)
    if not isinstance(rows, list):
        raise ValueError("artifact input must be a JSON array")
    artifacts: list[ArtifactRef] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each artifact row must be an object")
        artifacts.append(
            ArtifactRef(
                kind=str(row["kind"]),
                path=PurePosixPath(str(row["path"])),
                schema_version=str(row["schema_version"]),
                content_sha256=str(row["content_sha256"]),
            )
        )

    renderer = ManifestOnlyRenderer()
    manifest_path = renderer.render(
        artifacts,
        config,
        args.output,
        evidence_links={
            "case_id": args.case_id,
            "run_ids": args.run_id,
            "claim_ids": args.claim_id,
        },
    )[0]
    manifest = _load_json(manifest_path)
    manifest_schema = _load_json(ROOT / "schemas/render-manifest.schema.json")
    jsonschema.Draft202012Validator(manifest_schema).validate(manifest)
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
