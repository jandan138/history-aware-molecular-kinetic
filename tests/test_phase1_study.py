from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from historykinetic.studies import load_study_config, run_paired_study, write_study

ROOT = Path(__file__).resolve().parents[1]


def test_phase1_smoke_generates_ensemble_rows_and_hashed_manifest(
    tmp_path: Path,
) -> None:
    config = load_study_config(ROOT / "configs/studies/phase1-paper-story.json")
    smoke = replace(
        config,
        cases=config.cases[:2],
        seeds=config.seeds[:3],
        end_time=0.4,
        future_horizon=0.1,
        history_window=0.2,
        ensemble_group_size=3,
    )

    result = run_paired_study(smoke)
    dataset, manifest = write_study(result, tmp_path)

    assert result.rows
    assert len(result.audits) == 6
    assert all(row.ensemble_members == (0, 1, 2) for row in result.rows)
    assert all(
        visibility == "oracle_only"
        for row in result.rows
        for name, visibility in row.feature_visibility.items()
        if name.startswith("history_")
    )
    assert dataset.exists()
    assert manifest.exists()
    assert '"sha256":' in manifest.read_text(encoding="utf-8")


def test_phase1_story_is_complete_geometry_state_factorial() -> None:
    config = load_study_config(ROOT / "configs/studies/phase1-paper-story.json")
    combinations = {(case.geometry_id, case.state_id) for case in config.cases}

    assert len({case.geometry_id for case in config.cases}) == 3
    assert len({case.state_id for case in config.cases}) == 3
    assert len(combinations) == 9
