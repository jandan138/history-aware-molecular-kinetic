from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from .bundle import E6_SHOT_IDS, export_shots


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export frozen E6 renderer-neutral shot bundles")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--shot",
        action="append",
        choices=("all", *E6_SHOT_IDS),
        default=[],
        help="repeat to export several shots; defaults to all",
    )
    args = parser.parse_args(argv)
    selected = E6_SHOT_IDS if not args.shot or "all" in args.shot else tuple(args.shot)
    manifests = export_shots(args.repo_root.resolve(), args.output.resolve(), selected)
    for manifest in manifests:
        print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
