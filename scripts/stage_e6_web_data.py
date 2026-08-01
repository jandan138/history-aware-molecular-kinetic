#!/usr/bin/env python3
"""Stage generated E6 shot bundles for the static Three.js companion."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from historykinetic.e6 import E6_SHOT_IDS, export_shots


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.repo_root.resolve()
    generated = root / "results" / "molecular-time-machine-e6-v0" / "shot-bundles"
    staged = root / "demos" / "e6-web" / "public" / "shots"
    export_shots(root, generated)
    staged.mkdir(parents=True, exist_ok=True)
    for shot_id in E6_SHOT_IDS:
        destination = staged / shot_id
        shutil.copytree(generated / shot_id, destination, dirs_exist_ok=True)
        print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
