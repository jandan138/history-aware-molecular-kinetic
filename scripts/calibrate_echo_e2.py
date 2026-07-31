from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from statistics import mean

from historykinetic.e2 import calibrate_e2_budget, load_e2_protocol


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Select the E2 middle budget using excluded collision-dose data only."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/studies/molecular-echoes-e2-v0.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = calibrate_e2_budget(load_e2_protocol(args.config))
    dose_by_branch = {
        budget.branch_name: mean(
            row.collision_dose
            for row in result.rows
            if row.branch == budget.branch_name
        )
        for budget in result.protocol.budgets
    }
    payload = {
        "schema_version": "1.0.0",
        "study_id": result.protocol.study_id,
        "evidence_scope": "excluded calibration seeds; collision dose only",
        "passive_color_observable_accessed": False,
        "selection_rule": "mean dose closest to 0.5; lexical tie break",
        "selected_branch": result.selected_branch,
        "mean_collision_dose_by_branch": dose_by_branch,
        "rows": [
            {
                **asdict(row),
                "direction": row.direction.value,
            }
            for row in result.rows
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
