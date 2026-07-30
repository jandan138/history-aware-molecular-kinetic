from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema

from historykinetic.rendering import audit_manifests

ROOT = Path(__file__).resolve().parents[1]


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit render manifests for a fair primary method comparison."
    )
    parser.add_argument("manifests", type=Path, nargs="+")
    parser.add_argument(
        "--require-complete-evidence",
        action="store_true",
        help="Require complete case/run/claim/metric linkage for every manifest.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    schema = _load_object(ROOT / "schemas" / "render-manifest.schema.json")
    validator = jsonschema.Draft202012Validator(schema)
    manifests = [_load_object(path) for path in args.manifests]
    for path, manifest in zip(args.manifests, manifests, strict=True):
        try:
            validator.validate(manifest)
        except jsonschema.ValidationError as exc:
            raise ValueError(f"invalid render manifest {path}: {exc.message}") from exc

    errors = audit_manifests(
        manifests,
        require_complete_evidence=args.require_complete_evidence,
    )
    if errors:
        print("render comparison audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"render comparison audit passed for {len(manifests)} manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
