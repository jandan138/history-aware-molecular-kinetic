from __future__ import annotations

import argparse
from pathlib import Path

from historykinetic.studies.decision import decide_phase1, load_json, write_decision


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a Go/Pivot/Stop report from Phase-I evidence."
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--evaluation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-improvement", type=float, default=0.05)
    parser.add_argument("--minimum-coverage-gain", type=float, default=0.03)
    args = parser.parse_args()
    report = decide_phase1(
        load_json(args.manifest),
        load_json(args.evaluation),
        minimum_operational_mae_improvement=args.minimum_improvement,
        minimum_coverage_gain=args.minimum_coverage_gain,
    )
    json_path, markdown_path = write_decision(report, args.output)
    print(f"decision: {report['decision']}")
    print(f"json: {json_path}")
    print(f"markdown: {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
