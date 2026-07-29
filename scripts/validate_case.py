from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema
import yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case", type=Path)
    parser.add_argument("--schema", type=Path, default=Path("schemas/benchmark-case.schema.json"))
    args = parser.parse_args()
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    payload = yaml.safe_load(args.case.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(payload)
    print(f"valid: {args.case}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
