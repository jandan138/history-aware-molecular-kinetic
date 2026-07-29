from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from historykinetic.ids import content_id


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hamk")
    subparsers = parser.add_subparsers(dest="command", required=True)

    identifier = subparsers.add_parser("id", help="compute a stable content ID from JSON")
    identifier.add_argument("prefix")
    identifier.add_argument("json_file", type=Path)

    check = subparsers.add_parser("check", help="run repository structural checks")
    check.add_argument("--root", type=Path, default=Path.cwd())
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "id":
        payload = json.loads(args.json_file.read_text(encoding="utf-8"))
        print(content_id(args.prefix, payload))
        return 0
    if args.command == "check":
        import runpy

        runpy.run_path(str(args.root / "scripts" / "check_repo.py"), run_name="__main__")
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
