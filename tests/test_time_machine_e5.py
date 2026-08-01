from __future__ import annotations

import json
from pathlib import Path

import pytest

from historykinetic.e5 import (
    MolecularTimeMachineE5Result,
    load_e5_protocol,
    run_molecular_time_machine_e5,
)
from historykinetic.e5.artifacts import summarize_e5, write_e5_result

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs" / "studies" / "molecular-time-machine-e5-v0.json"


@pytest.fixture(scope="module")
def hero_result() -> MolecularTimeMachineE5Result:
    return run_molecular_time_machine_e5(load_e5_protocol(PROTOCOL_PATH))


def test_same_present_surgery_authors_the_registered_e_to_c_future(
    hero_result: MolecularTimeMachineE5Result,
) -> None:
    selected = hero_result.selected_preview
    summary = summarize_e5(hero_result)

    assert hero_result.target.particle_ids == (15, 48, 65, 82, 99, 106, 174, 211)
    assert len(hero_result.previews) == 30
    assert selected.surgery.swaps == ((48, 82), (174, 211))
    assert selected.surgery.touched_particle_ids == (48, 82, 174, 211)
    assert selected.outcome.baseline_target_region_occupancy == 8
    assert selected.outcome.edited_target_region_occupancy == 2
    assert selected.outcome.target_ejection_fraction == 0.75
    assert selected.outcome.target_region_reduction_fraction == 0.75
    assert selected.outcome.collateral_retention_fraction == 1.0
    assert summary["decision"] == "go"


def test_selected_surgery_preserves_the_declared_present(
    hero_result: MolecularTimeMachineE5Result,
) -> None:
    audit = hero_result.selected_preview.audit

    assert audit.positions_identical
    assert audit.colors_identical
    assert audit.particle_arrays_identical_except_velocity_ownership
    assert audit.declared_cell_velocity_multisets_identical
    assert audit.declared_cell_target_velocity_multisets_identical
    assert audit.geometry_valid
    assert audit.mass_error == 0.0
    assert audit.momentum_error <= 1.0e-12
    assert audit.energy_error == 0.0
    assert hero_result.pivot_replay_audit.collision_pair_agreement == 1.0


def test_e5_writes_target_palette_surgery_and_resolved_present_audit(
    hero_result: MolecularTimeMachineE5Result,
    tmp_path: Path,
) -> None:
    paths = write_e5_result(
        hero_result,
        tmp_path,
        protocol_path=PROTOCOL_PATH,
        include_trajectories=False,
    )
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    palette = json.loads(paths["palette"].read_text(encoding="utf-8"))
    surgery = json.loads(paths["surgery"].read_text(encoding="utf-8"))
    audit = json.loads(paths["audit"].read_text(encoding="utf-8"))

    assert len(palette["previews"]) == 30
    assert surgery["surgery"]["swaps"] == [[48, 82], [174, 211]]
    assert audit["audit"]["declared_cell_velocity_multisets_identical"] is True
    assert manifest["artifacts"]["surgery-preview-palette.json"]["sha256"]
    assert manifest["artifacts"]["selected-surgery-manifest.json"]["sha256"]
