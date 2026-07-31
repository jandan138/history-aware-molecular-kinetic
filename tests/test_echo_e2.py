from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from historykinetic.e2 import (
    E2Direction,
    MolecularEchoesE2Protocol,
    load_e2_protocol,
    run_e2,
    summarize_e2,
    write_e2_result,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs" / "studies" / "molecular-echoes-e2-v0.json"


def _smoke_protocol() -> MolecularEchoesE2Protocol:
    protocol = load_e2_protocol(PROTOCOL_PATH)
    e1 = protocol.e1_protocol
    size = replace(e1.sizes[0], count=32, diameter=5.12 / 32)
    e1 = replace(
        e1,
        sizes=(size,),
        seeds=(0,),
        preparation_time=0.2,
        future_horizon=0.2,
        sample_interval=0.05,
        bootstrap_resamples=200,
        render=replace(e1.render, hero_particle_count=32),
    )
    return replace(
        protocol,
        e1_protocol=e1,
        seeds=(0,),
        calibration_particle_count=32,
        bootstrap_resamples=200,
        render=replace(protocol.render, hero_particle_count=32),
    )


def test_e2_protocol_freezes_dose_only_calibration_and_primary_scope() -> None:
    protocol = load_e2_protocol(PROTOCOL_PATH)

    assert protocol.selected_budget.branch_name == "budget-l4-g0"
    assert protocol.seeds == (0, 1, 2, 3, 4, 5)
    assert protocol.calibration_seeds == (100, 101)
    assert not set(protocol.seeds) & set(protocol.calibration_seeds)
    assert tuple(budget.branch_name for budget in protocol.budgets) == (
        "budget-l4-g0",
        "budget-l8-g0",
        "budget-l16-g1",
    )


def test_e2_smoke_runs_ladder_and_two_selected_budget_controls(tmp_path: Path) -> None:
    protocol = _smoke_protocol()
    result = run_e2(protocol)

    assert len(result.cases) == 1
    case = result.cases[0]
    assert len(case.branches) == 2 * len(protocol.branch_names)
    for direction in E2Direction:
        full = case.branch(direction, "full").result
        ghost = case.branch(direction, "ghost").result
        assert len(full.accepted_encounters) == len(full.encounter_events)
        assert len(ghost.suppressed_encounters) == len(ghost.encounter_events)
        assert ghost.simulation.collision_events == ()

    calibration_path = tmp_path / "calibration.json"
    calibration_path.write_text(
        json.dumps({"selected_branch": "budget-l4-g0"}) + "\n",
        encoding="utf-8",
    )
    paths = write_e2_result(
        result,
        tmp_path / "result",
        protocol_path=PROTOCOL_PATH,
        calibration_path=calibration_path,
        include_trajectories=False,
    )
    summary = summarize_e2(result)
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    assert summary["decision"] in {"go", "narrow", "stop_e2"}
    assert manifest["artifacts"]["encounter-events.jsonl.gz"]["sha256"]
