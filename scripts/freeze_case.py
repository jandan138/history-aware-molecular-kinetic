from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from historykinetic.ids import content_id


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy a reviewed candidate case into its frozen directory."
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    relative = args.candidate.resolve().relative_to(args.root.resolve())
    parts = list(relative.parts)
    try:
        index = parts.index("candidate")
    except ValueError as exc:
        raise SystemExit("candidate path must contain cases/candidate") from exc
    parts[index] = "frozen"
    target = args.root.joinpath(*parts)
    if target.exists():
        raise SystemExit(f"frozen case already exists: {target}")
    raw = args.candidate.read_text(encoding="utf-8")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.candidate, target)
    print(f"frozen {relative} -> {target.relative_to(args.root)} ({content_id('case', raw)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
