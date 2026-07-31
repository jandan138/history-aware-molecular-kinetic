from __future__ import annotations

import json
from pathlib import Path

import pytest

from historykinetic.e3 import (
    MolecularTimeMachineE3Result,
    load_e3_protocol,
    run_molecular_time_machine_e3,
    summarize_e3,
    write_e3_result,
)
from historykinetic.timeline import CollisionCausalGraph

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs" / "studies" / "molecular-time-machine-e3-v0.json"


@pytest.fixture(scope="module")
def hero_result() -> MolecularTimeMachineE3Result:
    return run_molecular_time_machine_e3(load_e3_protocol(PROTOCOL_PATH))


def test_one_collision_two_worlds_recipe_passes_its_story_gate(
    hero_result: MolecularTimeMachineE3Result,
) -> None:
    graph = CollisionCausalGraph(hero_result.timeline.events)
    target = hero_result.target_event
    summary = summarize_e3(hero_result)

    assert target.ordinal == 2
    assert target.pair == (101, 118)
    assert target.time == pytest.approx(0.03429093183046455, abs=1.0e-12)
    assert len(graph.descendant_particles(target.event_id)) == 20
    assert summary["decision"] == "go"
    assert all(summary["checks"].values())
    assert hero_result.metrics.terminal_color_gap >= 0.15
    assert hero_result.metrics.visibly_changed_particle_count == 33
    assert hero_result.branch.comparison.collision_pair_agreement == 1.0
    assert hero_result.branch.local.diagnostics.baseline_event_reuse_fraction >= 0.50


def test_e3_writes_traceable_branch_artifacts(
    hero_result: MolecularTimeMachineE3Result,
    tmp_path: Path,
) -> None:
    paths = write_e3_result(
        hero_result,
        tmp_path,
        protocol_path=PROTOCOL_PATH,
        include_trajectories=False,
    )
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    edit = json.loads(paths["edit"].read_text(encoding="utf-8"))
    comparison = json.loads(paths["comparison"].read_text(encoding="utf-8"))

    assert manifest["artifacts"]["collision-timeline.jsonl"]["sha256"]
    assert manifest["artifacts"]["checkpoints.json.gz"]["sha256"]
    assert edit["target_event_id"] == "collision-000002"
    assert edit["conservation"]["momentum_error"] <= 1.0e-12
    assert comparison["collision_pair_agreement"] == 1.0
