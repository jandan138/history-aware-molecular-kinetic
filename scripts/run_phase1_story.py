from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

from historykinetic.studies import load_study_config, run_paired_study, write_study


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the paired EDMD-DSMC dataset for the Phase-I paper story."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/studies/phase1-paper-story.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="run two cases, one seed, and a short horizon for pipeline verification",
    )
    args = parser.parse_args()

    config = load_study_config(args.config)
    if args.smoke:
        config = replace(
            config,
            cases=config.cases[:2],
            seeds=config.seeds[:1],
            end_time=0.6,
            preparation_time=0.3,
            future_horizon=0.2,
            history_window=0.3,
            ensemble_group_size=1,
        )
    result = run_paired_study(config)
    dataset_path, manifest_path = write_study(result, args.output)
    print(
        f"wrote {len(result.rows)} paired rows from {len(result.audits)} runs: "
        f"{dataset_path}"
    )
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
