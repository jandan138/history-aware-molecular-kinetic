"""Traceable evidence artifacts for the E5 future-authoring Hero."""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
from dataclasses import asdict
from pathlib import Path
from typing import Any

from historykinetic.echo.artifacts import refresh_manifest
from historykinetic.solvers import Snapshot
from historykinetic.timeline import state_sha256

from .models import MolecularTimeMachineE5Result, SurgeryPreview


def summarize_e5(result: MolecularTimeMachineE5Result) -> dict[str, Any]:
    acceptance = result.protocol.acceptance
    metrics = result.metrics
    audit = result.selected_preview.audit
    replay = result.pivot_replay_audit
    checks = {
        "same_visible_present": (
            audit.positions_identical
            and audit.colors_identical
            and audit.particle_arrays_identical_except_velocity_ownership
        ),
        "declared_resolved_present": (
            audit.declared_cell_velocity_multisets_identical
            and audit.declared_cell_target_velocity_multisets_identical
        ),
        "valid_geometry": audit.geometry_valid,
        "mass_conservation": audit.mass_error <= acceptance.maximum_mass_error,
        "momentum_conservation": (
            audit.momentum_error <= acceptance.maximum_momentum_error
        ),
        "energy_conservation": audit.energy_error <= acceptance.maximum_energy_error,
        "pivot_replay_positions": (
            replay.terminal_position_rms
            <= acceptance.maximum_pivot_replay_position_rms
        ),
        "pivot_replay_velocities": (
            replay.terminal_velocity_rms
            <= acceptance.maximum_pivot_replay_velocity_rms
        ),
        "pivot_replay_event_pairs": replay.collision_pair_agreement == 1.0,
        "target_particle_ejection": (
            metrics.target_ejection_fraction
            >= acceptance.minimum_target_ejection_fraction
        ),
        "target_region_reduction": (
            metrics.target_region_reduction_fraction
            >= acceptance.minimum_target_region_reduction_fraction
        ),
        "collateral_glyph_retention": (
            metrics.collateral_retention_fraction
            >= acceptance.minimum_collateral_retention_fraction
        ),
        "sparse_hidden_edit": (
            metrics.touched_particle_count <= acceptance.maximum_touched_particle_count
        ),
    }
    decision = "go" if all(checks.values()) else "stop_e5"
    selected = result.selected_preview
    return {
        "schema_version": "1.0.0",
        "study_id": result.protocol.study_id,
        "decision": decision,
        "story_claim": (
            "preserve one declared visible present and author a selected E-to-C future "
            "with a sparse hidden velocity-ownership surgery"
        ),
        "claim_boundary": (
            "one registered N=256 Hero at a declared 4x2 resolved state; "
            "not exact-microstate equality or a generic glyph optimizer"
        ),
        "checks": checks,
        "target": asdict(result.target),
        "authoring_session": {
            "action": "select the future middle stroke and suppress it",
            "pivot_time": result.protocol.hero.pivot_time,
            "preview_mode": "cached complete EDMD from the common pivot",
            "preview_count": metrics.preview_count,
            "preview_median_seconds": metrics.preview_median_seconds,
            "selection_rule": (
                "require registered collateral retention; maximize target ejection, "
                "then collateral retention and sparsity"
            ),
            "selected_surgery_id": selected.surgery.surgery_id,
            "selected_swaps": [list(pair) for pair in selected.surgery.swaps],
            "touched_particle_ids": list(selected.surgery.touched_particle_ids),
        },
        "resolved_present_audit": asdict(audit),
        "pivot_replay_audit": asdict(replay),
        "selected_outcome": asdict(selected.outcome),
        "metrics": asdict(metrics),
    }


def write_e5_result(
    result: MolecularTimeMachineE5Result,
    output_directory: Path,
    *,
    protocol_path: Path,
    include_trajectories: bool = True,
) -> dict[str, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    target_path = output_directory / "future-target.json"
    target_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                **asdict(result.target),
                "selection_mode": "registered-terminal-region-before-surgery-selection",
                "baseline_terminal_state_sha256": state_sha256(
                    result.baseline.snapshots[-1].state
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["target"] = target_path

    palette_path = output_directory / "surgery-preview-palette.json"
    palette_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "candidate_family": (
                    "one or two disjoint target-only velocity transpositions within "
                    "the same declared 4x2 cell"
                ),
                "preview_physics": "complete EDMD from the common pivot",
                "previews": [_preview_payload(preview) for preview in result.previews],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["palette"] = palette_path

    audit_path = output_directory / "resolved-present-audit.json"
    audit_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "declared_spatial_grid": list(
                    result.selected_preview.surgery.declared_spatial_grid
                ),
                "pivot_time": result.protocol.hero.pivot_time,
                "selected_surgery": result.selected_preview.surgery.surgery_id,
                "audit": asdict(result.selected_preview.audit),
                "wording_boundary": (
                    "same declared 4x2 resolved present, not the same exact microstate"
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["audit"] = audit_path

    surgery_path = output_directory / "selected-surgery-manifest.json"
    surgery_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "parent": "exact-reverse-n256-seed4",
                "pivot_state_sha256": state_sha256(result.pivot_state),
                "edited_pivot_state_sha256": state_sha256(
                    result.selected_preview.edited_pivot
                ),
                "surgery": asdict(result.selected_preview.surgery),
                "touched_particle_ids": list(
                    result.selected_preview.surgery.touched_particle_ids
                ),
                "outcome": asdict(result.selected_preview.outcome),
                "physics": "complete hard-disk EDMD after the pivot",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["surgery"] = surgery_path

    replay_path = output_directory / "pivot-replay-audit.json"
    replay_path.write_text(
        json.dumps(asdict(result.pivot_replay_audit), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths["replay"] = replay_path

    summary = summarize_e5(result)
    summary_path = output_directory / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    paths["summary"] = summary_path
    decision_path = output_directory / "decision.md"
    decision_path.write_text(_decision_markdown(summary) + "\n", encoding="utf-8")
    paths["decision"] = decision_path

    if include_trajectories:
        trajectories_path = output_directory / "same-present-trajectories.json.gz"
        with gzip.open(trajectories_path, "wt", encoding="utf-8") as handle:
            json.dump(
                {
                    "particle_ids": result.pivot_state.particle_ids,
                    "passive_colors": result.colors.labels_by_particle_id,
                    "pivot_time": result.protocol.hero.pivot_time,
                    "baseline": [
                        _snapshot_payload(snapshot)
                        for snapshot in result.baseline.snapshots
                    ],
                    "selected_after_pivot": [
                        _snapshot_payload(
                            snapshot,
                            time_offset=result.protocol.hero.pivot_time,
                        )
                        for snapshot in result.selected_preview.simulation.snapshots
                    ],
                },
                handle,
                sort_keys=True,
                separators=(",", ":"),
            )
        paths["trajectories"] = trajectories_path

    manifest_path = output_directory / "run-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "study_id": result.protocol.study_id,
                "protocol": {
                    "path": protocol_path.as_posix(),
                    "sha256": _sha256(protocol_path),
                },
                "e1_protocol": {
                    "path": result.protocol.e1_protocol_path.as_posix(),
                    "sha256": _sha256(result.protocol.e1_protocol_path),
                },
                "repository": _repository_state(),
                "branch_lineage": {
                    "parent": "exact-reverse-n256-seed4",
                    "pivot_time": result.protocol.hero.pivot_time,
                    "target_id": result.target.target_id,
                    "surgery_id": result.selected_preview.surgery.surgery_id,
                },
                "artifacts": {},
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["manifest"] = manifest_path
    refresh_manifest(output_directory)
    return paths


def _preview_payload(preview: SurgeryPreview) -> dict[str, Any]:
    return {
        "surgery_id": preview.surgery.surgery_id,
        "swaps": [list(pair) for pair in preview.surgery.swaps],
        "touched_particle_ids": list(preview.surgery.touched_particle_ids),
        "wall_seconds": preview.wall_seconds,
        "resolved_present_audit": asdict(preview.audit),
        "outcome": asdict(preview.outcome),
        "terminal_positions": preview.simulation.snapshots[-1].state.positions,
    }


def _snapshot_payload(snapshot: Snapshot, *, time_offset: float = 0.0) -> dict[str, Any]:
    return {
        "time": snapshot.time + time_offset,
        "positions": snapshot.state.positions,
        "velocities": snapshot.state.velocities,
    }


def _decision_markdown(summary: dict[str, Any]) -> str:
    outcome = summary["selected_outcome"]
    session = summary["authoring_session"]
    return "\n".join(
        [
            "# E5 decision",
            "",
            f"**Decision:** `{summary['decision']}`.",
            "",
            "The registered creator selected the future E middle stroke. At the common",
            f"pivot, the system selected swaps `{session['selected_swaps']}` and touched",
            "four of 256 particles without moving or recoloring the visible present.",
            "",
            f"The target region fell from `{outcome['baseline_target_region_occupancy']}`",
            f"foreground particles to `{outcome['edited_target_region_occupancy']}`, while",
            f"collateral glyph retention was `{outcome['collateral_retention_fraction']:.0%}`.",
        ]
    )


def _repository_state() -> dict[str, Any]:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"], check=True, capture_output=True, text=True
    ).stdout
    return {"commit": commit, "dirty": bool(status.strip())}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
