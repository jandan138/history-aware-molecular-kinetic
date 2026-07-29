from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    date = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
    target = args.root / "experiments" / "registry" / f"{date}-{args.slug}"
    if target.exists():
        raise SystemExit(f"experiment already exists: {target}")
    target.mkdir(parents=True)
    template = args.root / "experiments" / "templates" / "experiment.yml"
    shutil.copy2(template, target / "experiment.yml")
    (target / "README.md").write_text(f"# {args.slug}\n\nRegistered {date}.\n", encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
