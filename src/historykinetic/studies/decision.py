"""Convert Phase-I evidence into a predeclared Go/Pivot/Stop decision."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def decide_phase1(
    manifest: dict[str, Any],
    evaluation: dict[str, Any],
    *,
    minimum_operational_mae_improvement: float = 0.05,
    minimum_coverage_gain: float = 0.03,
    energy_tolerance: float = 1.0e-12,
) -> dict[str, Any]:
    audits = manifest["audits"]
    maximum_exact_energy_error = max(
        float(audit["exact_relative_energy_error"]) for audit in audits
    )
    maximum_kinetic_energy_error = max(
        float(audit["kinetic_relative_energy_error"]) for audit in audits
    )
    aggregate = evaluation["aggregate"]
    bootstrap = aggregate["grouped_bootstrap"]
    observed_improvement = float(aggregate["mean_relative_mae_improvement"])
    coverage_gain = float(aggregate["mean_history_high_error_coverage"]) - float(
        aggregate["mean_state_high_error_coverage"]
    )
    geometry_count = len(manifest["groups"]["geometry_ids"])
    state_count = len(manifest["groups"]["state_ids"])
    credibility = {
        "exact_energy_within_tolerance": maximum_exact_energy_error <= energy_tolerance,
        "kinetic_energy_within_tolerance": maximum_kinetic_energy_error
        <= energy_tolerance,
        "complete_geometry_state_axes": geometry_count >= 3 and state_count >= 3,
        "trajectory_groups_present": int(manifest["groups"]["trajectory_groups"]) >= 18,
        "state_model_oracle_leakage_absent": evaluation["observability"][
            "state_model_uses_oracle_only"
        ]
        is False,
    }
    credible = all(credibility.values())

    if not credible:
        decision = "inconclusive"
        reason = "minimum benchmark credibility checks did not all pass"
    elif (
        float(bootstrap["ci95_low"]) >= minimum_operational_mae_improvement
        and coverage_gain >= minimum_coverage_gain
    ):
        decision = "go_history_aware"
        reason = "history clears both predictive and fixed-budget operational margins"
    elif float(bootstrap["ci95_high"]) < minimum_operational_mae_improvement:
        decision = "stop_history_claim"
        reason = (
            "the grouped/OOD confidence interval lies below the predeclared "
            "operational improvement margin"
        )
    else:
        decision = "inconclusive"
        reason = "the interval overlaps the operational margin"

    return {
        "schema_version": "1.0.0",
        "study_id": manifest["study_id"],
        "target": evaluation["target"],
        "model_kind": evaluation["model_kind"],
        "decision": decision,
        "reason": reason,
        "thresholds": {
            "minimum_operational_mae_improvement": minimum_operational_mae_improvement,
            "minimum_coverage_gain": minimum_coverage_gain,
            "energy_tolerance": energy_tolerance,
        },
        "credibility": {
            **credibility,
            "maximum_exact_relative_energy_error": maximum_exact_energy_error,
            "maximum_kinetic_relative_energy_error": maximum_kinetic_energy_error,
            "geometry_count": geometry_count,
            "state_count": state_count,
            "run_count": len(audits),
            "dataset_row_count": manifest["dataset"]["row_count"],
        },
        "result": {
            "mean_relative_mae_improvement": observed_improvement,
            "grouped_bootstrap_ci95": [
                float(bootstrap["ci95_low"]),
                float(bootstrap["ci95_high"]),
            ],
            "state_high_error_coverage": float(
                aggregate["mean_state_high_error_coverage"]
            ),
            "history_high_error_coverage": float(
                aggregate["mean_history_high_error_coverage"]
            ),
            "coverage_gain": coverage_gain,
            "state_oracle_residual_error_fraction": float(
                aggregate["mean_state_residual_error_fraction"]
            ),
            "history_oracle_residual_error_fraction": float(
                aggregate["mean_history_residual_error_fraction"]
            ),
        },
    }


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_decision(report: dict[str, Any], output: Path) -> tuple[Path, Path]:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown = output.with_suffix(".md")
    result = report["result"]
    credibility = report["credibility"]
    markdown.write_text(
        "\n".join(
            [
                f"# {report['study_id']} decision",
                "",
                f"**Decision:** `{report['decision']}`",
                "",
                str(report["reason"]) + ".",
                "",
                "## Core result",
                "",
                (
                    "- Grouped/OOD relative MAE improvement: "
                    f"{100.0 * result['mean_relative_mae_improvement']:.2f}%"
                ),
                (
                    "- Grouped bootstrap 95% interval: "
                    f"[{100.0 * result['grouped_bootstrap_ci95'][0]:.2f}%, "
                    f"{100.0 * result['grouped_bootstrap_ci95'][1]:.2f}%]"
                ),
                (
                    "- High-error coverage at fixed budget: "
                    f"{result['state_high_error_coverage']:.3f} state-only vs "
                    f"{result['history_high_error_coverage']:.3f} state+history"
                ),
                "",
                "## Benchmark credibility",
                "",
                f"- Runs: {credibility['run_count']}",
                f"- Dataset rows: {credibility['dataset_row_count']}",
                (
                    "- Maximum exact relative energy error: "
                    f"{credibility['maximum_exact_relative_energy_error']:.3e}"
                ),
                (
                    "- Maximum kinetic relative energy error: "
                    f"{credibility['maximum_kinetic_relative_energy_error']:.3e}"
                ),
                "",
                "This report is an internal Phase-I decision, not a paper claim.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return output, markdown
