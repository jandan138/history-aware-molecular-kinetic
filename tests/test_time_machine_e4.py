from __future__ import annotations

import json
from pathlib import Path

import pytest

from historykinetic.e4 import (
    MolecularTimeMachineE4Result,
    load_e4_protocol,
    run_molecular_time_machine_e4,
    summarize_e4,
    write_e4_result,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs" / "studies" / "molecular-time-machine-e4-v0.json"


@pytest.fixture(scope="module")
def hero_result() -> MolecularTimeMachineE4Result:
    return run_molecular_time_machine_e4(load_e4_protocol(PROTOCOL_PATH))


def test_causal_steering_selects_a_future_feature_then_finds_one_past_cause(
    hero_result: MolecularTimeMachineE4Result,
) -> None:
    summary = summarize_e4(hero_result)
    selected = hero_result.selected_preview

    assert hero_result.target.particle_ids == (69, 76, 101, 106)
    assert tuple(candidate.event.ordinal for candidate in hero_result.candidates) == (4, 2, 12)
    assert selected.candidate.rank == 1
    assert selected.candidate.event.pair == (101, 111)
    assert selected.angle_degrees == -1.0
    assert len(hero_result.palette) == 12
    assert selected.target_metrics.target_ejection_fraction == 0.50
    assert selected.target_metrics.collateral_ejection_fraction == 0.125
    assert selected.target_metrics.target_to_collateral_ratio == 4.0
    assert hero_result.metrics.preview_median_seconds < 0.20
    assert hero_result.selected_branch.comparison.collision_pair_agreement == 1.0
    assert summary["decision"] == "go"
    assert all(summary["checks"].values())


def test_e4_writes_target_ranking_palette_and_one_verified_branch(
    hero_result: MolecularTimeMachineE4Result,
    tmp_path: Path,
) -> None:
    paths = write_e4_result(
        hero_result,
        tmp_path,
        protocol_path=PROTOCOL_PATH,
        include_trajectories=False,
    )
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    target = json.loads(paths["target"].read_text(encoding="utf-8"))
    ranking = json.loads(paths["ranking"].read_text(encoding="utf-8"))
    palette = json.loads(paths["palette"].read_text(encoding="utf-8"))
    session = json.loads(paths["session"].read_text(encoding="utf-8"))
    comparison = json.loads(paths["comparison"].read_text(encoding="utf-8"))

    assert target["particle_ids"] == [69, 76, 101, 106]
    assert ranking["baseline_only"] is True
    assert [candidate["ordinal"] for candidate in ranking["candidates"]] == [4, 2, 12]
    assert palette["full_resimulation_per_preview"] is False
    assert len(palette["previews"]) == 12
    assert session["actions"][-1]["action"] == "save_selected_branch_and_verify_once"
    assert comparison["collision_pair_agreement"] == 1.0
    assert manifest["artifacts"]["branch-palette.json"]["sha256"]
    assert manifest["artifacts"]["selected-branch-comparison.json"]["sha256"]
