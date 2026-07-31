from __future__ import annotations

import argparse
from pathlib import Path

from historykinetic.studies.evaluate import evaluate_grouped, load_dataset, write_evaluation


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate state-only versus state+history on grouped Phase-I splits."
    )
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--model",
        choices=("hist_gradient_boosting", "ridge"),
        default="hist_gradient_boosting",
    )
    parser.add_argument(
        "--target",
        choices=(
            "future_composite_error",
            "future_density_error",
            "future_temperature_error",
            "future_velocity_error",
            "future_distribution_error",
        ),
        default="future_composite_error",
    )
    parser.add_argument("--bootstrap", type=int, default=500)
    parser.add_argument(
        "--maximum-time-since-release",
        type=float,
        default=None,
    )
    args = parser.parse_args()
    report = evaluate_grouped(
        load_dataset(args.dataset),
        model_kind=args.model,
        target_name=args.target,
        maximum_time_since_release=args.maximum_time_since_release,
        bootstrap_repetitions=args.bootstrap,
    )
    write_evaluation(report, args.output)
    aggregate = report["aggregate"]
    print(
        "mean relative MAE improvement: "
        f"{100.0 * aggregate['mean_relative_mae_improvement']:.2f}%"
    )
    print(
        "grouped bootstrap 95% CI: "
        f"[{100.0 * aggregate['grouped_bootstrap']['ci95_low']:.2f}%, "
        f"{100.0 * aggregate['grouped_bootstrap']['ci95_high']:.2f}%]"
    )
    print(f"report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
