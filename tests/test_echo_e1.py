from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from historykinetic.echo import (
    EchoBranchKind,
    ParticleSize,
    audit_resolved_state,
    chaotize_velocities,
    load_echo_protocol,
    prepare_echo_initial_state,
    reverse_state,
    run_echo_e1,
)
from historykinetic.echo.artifacts import summarize_echo_e1, write_echo_e1_result
from historykinetic.echo.audit import invariant_mismatch

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs" / "studies" / "molecular-echoes-e1-v0.json"


def _protocol() -> object:
    return load_echo_protocol(PROTOCOL_PATH)


def test_echo_initial_state_has_registered_component_temperatures() -> None:
    protocol = load_echo_protocol(PROTOCOL_PATH)
    state, colors = prepare_echo_initial_state(protocol, particle_count=128, seed=0)

    mean_x = sum(velocity[0] for velocity in state.velocities) / state.particle_count
    mean_y = sum(velocity[1] for velocity in state.velocities) / state.particle_count
    tx = (
        protocol.particle_mass
        * sum((velocity[0] - mean_x) ** 2 for velocity in state.velocities)
        / state.particle_count
    )
    ty = (
        protocol.particle_mass
        * sum((velocity[1] - mean_y) ** 2 for velocity in state.velocities)
        / state.particle_count
    )

    assert mean_x == pytest.approx(0.0, abs=1.0e-14)
    assert mean_y == pytest.approx(0.0, abs=1.0e-14)
    assert tx == pytest.approx(protocol.temperature_x, abs=1.0e-14)
    assert ty == pytest.approx(protocol.temperature_y, abs=1.0e-14)
    assert set(colors.labels_by_particle_id) == {0, 1}


def test_chaotization_preserves_registered_resolved_state_and_invariants() -> None:
    protocol = load_echo_protocol(PROTOCOL_PATH)
    state, colors = prepare_echo_initial_state(protocol, particle_count=128, seed=0)
    reference = reverse_state(state)
    candidate, changed_fraction = chaotize_velocities(
        reference,
        colors,
        protocol,
        seed=0,
    )

    assert candidate.positions == reference.positions
    assert candidate.particle_ids == reference.particle_ids
    assert changed_fraction >= protocol.acceptance.minimum_changed_particle_fraction
    assert invariant_mismatch(reference, candidate) <= 1.0e-15
    for edges in protocol.audit_velocity_edges_standardized:
        audit = audit_resolved_state(
            particle_count=128,
            seed=0,
            reference=reference,
            candidate=candidate,
            colors=colors,
            protocol=protocol,
            spatial_grid=protocol.chaotization_blocks,
            velocity_edges_standardized=edges,
        )
        assert audit.total_variation == pytest.approx(0.0)
        assert audit.maximum_momentum_mismatch == pytest.approx(0.0, abs=1.0e-15)
        assert audit.maximum_energy_mismatch == pytest.approx(0.0, abs=1.0e-15)


def test_echo_smoke_runs_all_branches_and_writes_hashed_artifacts(
    tmp_path: Path,
) -> None:
    original = load_echo_protocol(PROTOCOL_PATH)
    protocol = replace(
        original,
        sizes=(ParticleSize(count=32, diameter=5.12 / 32),),
        seeds=(0,),
        preparation_time=0.3,
        future_horizon=0.3,
        sample_interval=0.1,
        bootstrap_resamples=200,
        render=replace(original.render, hero_particle_count=32),
    )
    result = run_echo_e1(protocol)

    assert len(result.cases) == 1
    assert {branch.kind for branch in result.cases[0].branches} == set(EchoBranchKind)
    assert result.cases[0].branch(EchoBranchKind.GHOST).result.collision_events == ()
    assert result.cases[0].reversal_audit.event_pair_agreement == pytest.approx(1.0)

    paths = write_echo_e1_result(
        result,
        tmp_path,
        protocol_path=PROTOCOL_PATH,
        include_trajectories=False,
    )
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    summary = summarize_echo_e1(result)
    assert manifest["study_id"] == protocol.study_id
    assert manifest["artifacts"]["branch-metrics.jsonl"]["sha256"]
    assert summary["decision"] in {"go", "narrow", "stop_e1"}
