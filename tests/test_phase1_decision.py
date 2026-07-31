from historykinetic.studies.decision import decide_phase1


def _manifest() -> dict[str, object]:
    audit = {
        "exact_relative_energy_error": 1.0e-15,
        "kinetic_relative_energy_error": 1.0e-15,
    }
    return {
        "study_id": "PHASE1-TEST-v0",
        "audits": [audit] * 18,
        "dataset": {"row_count": 100},
        "groups": {
            "geometry_ids": ["g0", "g1", "g2"],
            "state_ids": ["s0", "s1", "s2"],
            "trajectory_groups": 18,
        },
    }


def _evaluation(ci: tuple[float, float], coverage_gain: float) -> dict[str, object]:
    return {
        "target": "future_composite_error",
        "model_kind": "hist_gradient_boosting",
        "observability": {"state_model_uses_oracle_only": False},
        "aggregate": {
            "mean_relative_mae_improvement": sum(ci) / 2,
            "mean_state_high_error_coverage": 0.4,
            "mean_history_high_error_coverage": 0.4 + coverage_gain,
            "mean_state_residual_error_fraction": 0.7,
            "mean_history_residual_error_fraction": 0.65,
            "grouped_bootstrap": {"ci95_low": ci[0], "ci95_high": ci[1]},
        },
    }


def test_phase1_decision_requires_operational_not_only_statistical_gain() -> None:
    report = decide_phase1(_manifest(), _evaluation((0.001, 0.01), 0.01))

    assert report["decision"] == "stop_history_claim"


def test_phase1_decision_goes_only_when_both_margins_clear() -> None:
    report = decide_phase1(_manifest(), _evaluation((0.06, 0.09), 0.04))

    assert report["decision"] == "go_history_aware"
