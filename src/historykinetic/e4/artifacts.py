"""Traceable evidence artifacts for the E4 causal-steering Hero."""

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
from historykinetic.timeline import CausalCheckpoint, CollisionCausalGraph, state_sha256

from .models import CausalCandidate, MolecularTimeMachineE4Result, PalettePreview


def summarize_e4(result: MolecularTimeMachineE4Result) -> dict[str, Any]:
    acceptance = result.protocol.acceptance
    metrics = result.metrics
    selected = result.selected_branch
    comparison = selected.comparison
    diagnostics = selected.local.diagnostics
    edit_audit = selected.local.edit_audit
    checks = {
        "causal_recommendation": metrics.selected_candidate_rank == 1,
        "directed_target_change": (
            metrics.target_ejection_fraction >= acceptance.minimum_target_ejection_fraction
        ),
        "target_selectivity": (
            metrics.target_to_collateral_ratio >= acceptance.minimum_target_to_collateral_ratio
        ),
        "interactive_preview": (
            metrics.preview_median_seconds <= acceptance.maximum_preview_median_seconds
        ),
        "history_reuse": (
            metrics.selected_branch_reuse_fraction
            >= acceptance.minimum_baseline_event_reuse_fraction
        ),
        "local_full_event_pairs": (
            comparison.collision_pair_agreement >= acceptance.minimum_collision_pair_agreement
        ),
        "local_full_event_times": (
            comparison.maximum_collision_time_error <= acceptance.maximum_collision_time_error
        ),
        "local_full_terminal_positions": (
            comparison.terminal_position_rms <= acceptance.maximum_terminal_position_rms
        ),
        "local_full_terminal_velocities": (
            comparison.terminal_velocity_rms <= acceptance.maximum_terminal_velocity_rms
        ),
        "edit_momentum": edit_audit.momentum_error <= acceptance.maximum_edit_momentum_error,
        "edit_energy": edit_audit.energy_error <= acceptance.maximum_edit_energy_error,
    }
    correctness_names = (
        "local_full_event_pairs",
        "local_full_event_times",
        "local_full_terminal_positions",
        "local_full_terminal_velocities",
        "edit_momentum",
        "edit_energy",
    )
    steering_names = (
        "causal_recommendation",
        "directed_target_change",
        "target_selectivity",
        "interactive_preview",
        "history_reuse",
    )
    if all(checks[name] for name in correctness_names + steering_names):
        decision = "go"
    elif all(checks[name] for name in correctness_names) and checks["interactive_preview"]:
        decision = "narrow"
    else:
        decision = "stop_e4"
    return {
        "schema_version": "1.0.0",
        "study_id": result.protocol.study_id,
        "decision": decision,
        "story_claim": (
            "select a future feature, locate a causal collision, and steer an exact new future"
        ),
        "checks": checks,
        "target": {
            **asdict(result.target),
            "selection_mode": "registered-terminal-region",
        },
        "ranking": [
            {
                "rank": candidate.rank,
                "event_id": candidate.event.event_id,
                "ordinal": candidate.event.ordinal,
                "pair": list(candidate.event.pair),
                "time": candidate.event.time,
                "coverage": candidate.coverage,
                "purity": candidate.purity,
                "causal_score": candidate.causal_score,
            }
            for candidate in result.candidates
        ],
        "authoring_session": {
            "preview_mode": "exact-local-causal-branch; full oracle only for saved branch",
            "preview_count": metrics.preview_count,
            "preview_median_seconds": metrics.preview_median_seconds,
            "selected_event_id": result.selected_preview.candidate.event.event_id,
            "selected_collision_ordinal": result.selected_preview.candidate.event.ordinal,
            "selected_pair": list(result.selected_preview.candidate.event.pair),
            "selected_angle_degrees": metrics.selected_angle_degrees,
            "target_metrics": asdict(result.selected_preview.target_metrics),
        },
        "causal_reuse": {
            **asdict(diagnostics),
            "baseline_event_reuse_fraction": diagnostics.baseline_event_reuse_fraction,
            "peak_affected_fraction": diagnostics.peak_affected_fraction,
        },
        "branch_correctness": asdict(comparison),
        "edit_conservation": asdict(edit_audit),
        "reference_wall_time_seconds": {
            **asdict(selected.timing),
            "claim_boundary": (
                "Python reference observation for the registered interaction; "
                "not a broad native-performance claim"
            ),
        },
    }


def write_e4_result(
    result: MolecularTimeMachineE4Result,
    output_directory: Path,
    *,
    protocol_path: Path,
    include_trajectories: bool = True,
) -> dict[str, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    timeline_path = output_directory / "collision-timeline.jsonl"
    timeline_path.write_text(
        "".join(
            json.dumps(asdict(event), sort_keys=True, separators=(",", ":")) + "\n"
            for event in result.timeline.events
        ),
        encoding="utf-8",
    )
    paths["timeline"] = timeline_path

    target_path = output_directory / "causal-target.json"
    target_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                **asdict(result.target),
                "baseline_terminal_state_sha256": state_sha256(
                    result.timeline.result.snapshots[-1].state
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["target"] = target_path

    ranking_path = output_directory / "collision-ranking.json"
    ranking_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "ranking_rule": (
                    "harmonic mean of target-descendant coverage and target-descendant purity"
                ),
                "baseline_only": True,
                "candidate_event_limit": result.protocol.ranking.candidate_event_limit,
                "candidates": [_candidate_payload(candidate) for candidate in result.candidates],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["ranking"] = ranking_path

    palette_path = output_directory / "branch-palette.json"
    palette_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "mode": "exact-local-causal-preview",
                "full_resimulation_per_preview": False,
                "previews": [_palette_payload(item) for item in result.palette],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["palette"] = palette_path

    session_path = output_directory / "authoring-session.json"
    session_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "session_id": "erase-one-stroke-v0",
                "actions": [
                    {
                        "action": "select_terminal_feature",
                        "target_id": result.target.target_id,
                        "particle_ids": list(result.target.particle_ids),
                    },
                    {
                        "action": "rank_past_collisions_from_baseline_ancestry",
                        "recommended_event_id": result.candidates[0].event.event_id,
                        "shortlist_event_ids": [
                            candidate.event.event_id for candidate in result.candidates
                        ],
                    },
                    {
                        "action": "browse_exact_preview_palette",
                        "preview_count": len(result.palette),
                        "cache_key": "event_id + angle_degrees",
                    },
                    {
                        "action": "save_selected_branch_and_verify_once",
                        "event_id": result.selected_preview.candidate.event.event_id,
                        "angle_degrees": result.selected_preview.angle_degrees,
                        "checkpoint_id": result.selected_checkpoint.checkpoint_id,
                    },
                ],
                "selection_rule": (
                    "maximize target ejection minus collateral ejection; "
                    "tie-break by smaller absolute angle"
                ),
                "selected_preview": _palette_payload(result.selected_preview),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["session"] = session_path

    checkpoints_path = output_directory / "checkpoints.json.gz"
    with gzip.open(checkpoints_path, "wt", encoding="utf-8") as handle:
        json.dump(
            {
                "schema_version": "1.0.0",
                "checkpoints": [
                    _checkpoint_payload(checkpoint) for checkpoint in result.timeline.checkpoints
                ]
                + [_checkpoint_payload(result.selected_checkpoint)],
            },
            handle,
            sort_keys=True,
            separators=(",", ":"),
        )
    paths["checkpoints"] = checkpoints_path

    branch_events_path = output_directory / "selected-branch-events.jsonl"
    branch_events_path.write_text(
        "".join(
            json.dumps(asdict(event), sort_keys=True, separators=(",", ":")) + "\n"
            for event in result.selected_branch.local.events
        ),
        encoding="utf-8",
    )
    paths["branch_events"] = branch_events_path

    edit_path = output_directory / "selected-edit-manifest.json"
    edit_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "parent_timeline": result.protocol.study_id,
                "target_event_id": result.selected_preview.candidate.event.event_id,
                "target_pair": list(result.selected_preview.candidate.event.pair),
                "target_time": result.selected_preview.candidate.event.time,
                "checkpoint_id": result.selected_checkpoint.checkpoint_id,
                "checkpoint_time": result.selected_checkpoint.time,
                "checkpoint_state_sha256": result.selected_checkpoint.state_sha256,
                "edit": asdict(result.selected_branch.local.edit),
                "edited_state_sha256": state_sha256(
                    result.selected_branch.local.simulation.snapshots[0].state
                ),
                "conservation": asdict(result.selected_branch.local.edit_audit),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["edit"] = edit_path

    graph = CollisionCausalGraph(result.timeline.events)
    cone_path = output_directory / "selected-causal-cone.json"
    cone_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "target_event_id": result.selected_preview.candidate.event.event_id,
                "baseline_descendant_event_ids": [
                    event.event_id
                    for event in graph.descendants(result.selected_preview.candidate.event.event_id)
                ],
                "baseline_descendant_particle_ids": list(
                    graph.descendant_particles(result.selected_preview.candidate.event.event_id)
                ),
                "edited_branch_affected_particle_ids": list(
                    result.selected_branch.local.affected_particle_ids
                ),
                "edited_branch_affected_history": [
                    {"time": time, "particle_ids": list(particle_ids)}
                    for time, particle_ids in result.selected_branch.local.affected_history
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["causal_cone"] = cone_path

    comparison_path = output_directory / "selected-branch-comparison.json"
    comparison_path.write_text(
        json.dumps(
            asdict(result.selected_branch.comparison),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["comparison"] = comparison_path

    summary = summarize_e4(result)
    summary_path = output_directory / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths["summary"] = summary_path
    decision_path = output_directory / "decision.md"
    decision_path.write_text(_decision_markdown(summary) + "\n", encoding="utf-8")
    paths["decision"] = decision_path

    if include_trajectories:
        trajectories_path = output_directory / "causal-steering-trajectories.json.gz"
        with gzip.open(trajectories_path, "wt", encoding="utf-8") as handle:
            json.dump(
                {
                    "particle_ids": result.timeline.initial_state.particle_ids,
                    "passive_colors": result.colors.labels_by_particle_id,
                    "baseline": [
                        _snapshot_payload(snapshot) for snapshot in result.timeline.result.snapshots
                    ],
                    "selected": [
                        _snapshot_payload(snapshot)
                        for snapshot in result.selected_branch.local.simulation.snapshots
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
                    "parent": "exact-reverse-hero",
                    "target_id": result.target.target_id,
                    "recommended_event_id": result.selected_preview.candidate.event.event_id,
                    "checkpoint_id": result.selected_checkpoint.checkpoint_id,
                    "edit_id": (
                        f"rotate-relative-velocity-{result.selected_preview.angle_degrees:+g}deg"
                    ),
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


def _candidate_payload(item: CausalCandidate) -> dict[str, Any]:
    return {
        "rank": item.rank,
        "event_id": item.event.event_id,
        "ordinal": item.event.ordinal,
        "pair": list(item.event.pair),
        "time": item.event.time,
        "descendant_particle_ids": list(item.descendant_particle_ids),
        "target_descendant_particle_ids": list(item.target_descendant_particle_ids),
        "coverage": item.coverage,
        "purity": item.purity,
        "causal_score": item.causal_score,
    }


def _palette_payload(item: PalettePreview) -> dict[str, Any]:
    diagnostics = item.preview.local.diagnostics
    return {
        "event_id": item.candidate.event.event_id,
        "candidate_rank": item.candidate.rank,
        "angle_degrees": item.angle_degrees,
        "local_seconds": item.preview.local_seconds,
        "target_metrics": asdict(item.target_metrics),
        "causal_reuse": {
            "baseline_event_reuse_fraction": diagnostics.baseline_event_reuse_fraction,
            "peak_affected_fraction": diagnostics.peak_affected_fraction,
            "terminal_affected_particle_count": diagnostics.terminal_affected_particle_count,
        },
    }


def _checkpoint_payload(item: CausalCheckpoint) -> dict[str, Any]:
    return {
        "checkpoint_id": item.checkpoint_id,
        "kind": item.kind,
        "time": item.time,
        "last_event_ordinal": item.last_event_ordinal,
        "state_sha256": item.state_sha256,
        "state": {
            "positions": item.state.positions,
            "velocities": item.state.velocities,
            "radii": item.state.radii,
            "masses": item.state.masses,
            "particle_ids": item.state.particle_ids,
            "weights": item.state.weights,
        },
    }


def _snapshot_payload(item: Snapshot) -> dict[str, Any]:
    return {
        "time": item.time,
        "positions": item.state.positions,
        "velocities": item.state.velocities,
    }


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


def _decision_markdown(summary: dict[str, Any]) -> str:
    checks = "\n".join(
        f"| {name} | {'PASS' if passed else 'FAIL'} |" for name, passed in summary["checks"].items()
    )
    session = summary["authoring_session"]
    reuse = summary["causal_reuse"]
    correctness = summary["branch_correctness"]
    target = session["target_metrics"]
    return (
        "# Molecular Time Machine E4 decision\n\n"
        f"**Decision:** `{summary['decision']}`\n\n"
        "## Story result\n\n"
        "The creator selected the recovered E's upper stroke.  Baseline ancestry "
        "ranked one past collision, then a small exact preview palette chose a "
        "conservative angle.  The saved branch changes the selected stroke more "
        "than the rest of the foreground while a single full resimulation verifies "
        "the final choice.\n\n"
        f"- selected collision: `{session['selected_event_id']}`;\n"
        f"- selected angle: `{session['selected_angle_degrees']:+g}°`;\n"
        f"- target ejection: `{target['target_ejection_fraction']:.6f}`;\n"
        f"- collateral ejection: `{target['collateral_ejection_fraction']:.6f}`;\n"
        f"- baseline-event reuse: `{reuse['baseline_event_reuse_fraction']:.6f}`;\n"
        f"- local/full event-pair agreement: "
        f"`{correctness['collision_pair_agreement']:.6f}`.\n\n"
        "## Frozen checks\n\n"
        "| Check | Result |\n"
        "|---|---|\n"
        f"{checks}"
    )
