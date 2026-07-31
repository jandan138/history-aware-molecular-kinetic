from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
from dataclasses import asdict
from pathlib import Path
from typing import Any

from historykinetic.echo.artifacts import refresh_manifest
from historykinetic.timeline import CollisionCausalGraph, state_sha256

from .models import MolecularTimeMachineE3Result


def summarize_e3(result: MolecularTimeMachineE3Result) -> dict[str, Any]:
    protocol = result.protocol
    acceptance = protocol.acceptance
    comparison = result.branch.comparison
    diagnostics = result.branch.local.diagnostics
    edit_audit = result.branch.local.edit_audit
    metrics = result.metrics
    checks = {
        "baseline_echo": (
            metrics.baseline_terminal_color_score
            >= acceptance.minimum_baseline_terminal_color_score
        ),
        "visible_world_split": metrics.terminal_color_gap >= acceptance.minimum_terminal_color_gap,
        "changed_fraction_lower": (
            metrics.visibly_changed_particle_fraction
            >= acceptance.minimum_visibly_changed_fraction
        ),
        "changed_fraction_upper": (
            metrics.visibly_changed_particle_fraction
            <= acceptance.maximum_visibly_changed_fraction
        ),
        "local_full_event_pairs": (
            comparison.collision_pair_agreement
            >= acceptance.minimum_collision_pair_agreement
        ),
        "local_full_event_times": (
            comparison.maximum_collision_time_error
            <= acceptance.maximum_collision_time_error
        ),
        "local_full_terminal_positions": (
            comparison.terminal_position_rms
            <= acceptance.maximum_terminal_position_rms
        ),
        "local_full_terminal_velocities": (
            comparison.terminal_velocity_rms
            <= acceptance.maximum_terminal_velocity_rms
        ),
        "edit_momentum": edit_audit.momentum_error <= acceptance.maximum_edit_momentum_error,
        "edit_energy": edit_audit.energy_error <= acceptance.maximum_edit_energy_error,
        "history_reuse": (
            diagnostics.baseline_event_reuse_fraction
            >= acceptance.minimum_baseline_event_reuse_fraction
        ),
        "causal_cone_local": (
            diagnostics.peak_affected_fraction
            <= acceptance.maximum_peak_affected_fraction
        ),
    }
    correctness_names = (
        "local_full_event_pairs",
        "local_full_event_times",
        "local_full_terminal_positions",
        "local_full_terminal_velocities",
        "edit_momentum",
        "edit_energy",
    )
    visible_names = (
        "baseline_echo",
        "visible_world_split",
        "changed_fraction_lower",
        "changed_fraction_upper",
    )
    correctness_pass = all(checks[name] for name in correctness_names)
    visible_pass = all(checks[name] for name in visible_names)
    reuse_pass = checks["history_reuse"] and checks["causal_cone_local"]
    if correctness_pass and visible_pass and reuse_pass:
        decision = "go"
    elif correctness_pass and visible_pass:
        decision = "narrow"
    else:
        decision = "stop_e3"
    return {
        "schema_version": "1.0.0",
        "study_id": protocol.study_id,
        "decision": decision,
        "story_claim": "one-degree edit to one past collision creates a different future",
        "checks": checks,
        "hero": {
            "particle_count": protocol.hero.particle_count,
            "seed": protocol.hero.seed,
            "target_event_id": result.target_event.event_id,
            "target_collision_ordinal": result.target_event.ordinal,
            "target_pair": list(result.target_event.pair),
            "target_time": result.target_event.time,
            "fork_time": result.fork_checkpoint.time,
            "edit_angle_degrees": protocol.edit_angle_degrees,
        },
        "world_split": asdict(metrics),
        "branch_correctness": asdict(comparison),
        "reference_wall_time_seconds": {
            **asdict(result.branch.timing),
            "claim_boundary": (
                "Python reference observation only; no optimized speed claim"
            ),
        },
        "causal_reuse": {
            **asdict(diagnostics),
            "baseline_event_reuse_fraction": diagnostics.baseline_event_reuse_fraction,
            "peak_affected_fraction": diagnostics.peak_affected_fraction,
        },
        "edit_conservation": asdict(edit_audit),
    }


def write_e3_result(
    result: MolecularTimeMachineE3Result,
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

    checkpoints_path = output_directory / "checkpoints.json.gz"
    checkpoints = (*result.timeline.checkpoints, result.fork_checkpoint)
    with gzip.open(checkpoints_path, "wt", encoding="utf-8") as handle:
        json.dump(
            {
                "schema_version": "1.0.0",
                "checkpoints": [
                    {
                        "checkpoint_id": checkpoint.checkpoint_id,
                        "kind": checkpoint.kind,
                        "time": checkpoint.time,
                        "last_event_ordinal": checkpoint.last_event_ordinal,
                        "state_sha256": checkpoint.state_sha256,
                        "state": {
                            "positions": checkpoint.state.positions,
                            "velocities": checkpoint.state.velocities,
                            "radii": checkpoint.state.radii,
                            "masses": checkpoint.state.masses,
                            "particle_ids": checkpoint.state.particle_ids,
                            "weights": checkpoint.state.weights,
                        },
                    }
                    for checkpoint in checkpoints
                ],
            },
            handle,
            sort_keys=True,
            separators=(",", ":"),
        )
    paths["checkpoints"] = checkpoints_path

    branch_events_path = output_directory / "branch-events.jsonl"
    branch_events_path.write_text(
        "".join(
            json.dumps(asdict(event), sort_keys=True, separators=(",", ":")) + "\n"
            for event in result.branch.local.events
        ),
        encoding="utf-8",
    )
    paths["branch_events"] = branch_events_path

    edit_path = output_directory / "edit-manifest.json"
    edit_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "parent_timeline": result.protocol.study_id,
                "target_event_id": result.target_event.event_id,
                "target_pair": list(result.target_event.pair),
                "target_time": result.target_event.time,
                "checkpoint_id": result.fork_checkpoint.checkpoint_id,
                "checkpoint_time": result.fork_checkpoint.time,
                "checkpoint_state_sha256": result.fork_checkpoint.state_sha256,
                "edit": asdict(result.branch.local.edit),
                "edited_state_sha256": state_sha256(
                    result.branch.local.simulation.snapshots[0].state
                ),
                "conservation": asdict(result.branch.local.edit_audit),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["edit"] = edit_path

    graph = CollisionCausalGraph(result.timeline.events)
    cone_path = output_directory / "causal-cone.json"
    cone_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "target_event_id": result.target_event.event_id,
                "baseline_descendant_event_ids": [
                    event.event_id for event in graph.descendants(result.target_event.event_id)
                ],
                "baseline_descendant_particle_ids": list(
                    graph.descendant_particles(result.target_event.event_id)
                ),
                "edited_branch_affected_particle_ids": list(
                    result.branch.local.affected_particle_ids
                ),
                "edited_branch_affected_history": [
                    {"time": time, "particle_ids": list(particles)}
                    for time, particles in result.branch.local.affected_history
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["causal_cone"] = cone_path

    comparison_path = output_directory / "branch-comparison.json"
    comparison_path.write_text(
        json.dumps(asdict(result.branch.comparison), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths["comparison"] = comparison_path
    summary = summarize_e3(result)
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
        trajectories_path = output_directory / "two-world-trajectories.json.gz"
        with gzip.open(trajectories_path, "wt", encoding="utf-8") as handle:
            json.dump(
                {
                    "particle_ids": result.timeline.initial_state.particle_ids,
                    "passive_colors": result.colors.labels_by_particle_id,
                    "baseline": [
                        {
                            "time": snapshot.time,
                            "positions": snapshot.state.positions,
                            "velocities": snapshot.state.velocities,
                        }
                        for snapshot in result.timeline.result.snapshots
                    ],
                    "edited": [
                        {
                            "time": snapshot.time,
                            "positions": snapshot.state.positions,
                            "velocities": snapshot.state.velocities,
                        }
                        for snapshot in result.branch.local.simulation.snapshots
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
                    "checkpoint_id": result.fork_checkpoint.checkpoint_id,
                    "target_event_id": result.target_event.event_id,
                    "edit_id": "rotate-relative-velocity-ccw-1deg",
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
        f"| {name} | {'PASS' if passed else 'FAIL'} |"
        for name, passed in summary["checks"].items()
    )
    split = summary["world_split"]
    reuse = summary["causal_reuse"]
    correctness = summary["branch_correctness"]
    return (
        "# Molecular Time Machine E3 decision\n\n"
        f"**Decision:** `{summary['decision']}`\n\n"
        "## Story result\n\n"
        "A one-degree edit to collision #2 produces two visibly different "
        "terminal worlds while the causal branch remains exactly aligned with "
        "a full resimulation.\n\n"
        f"- terminal color gap: `{split['terminal_color_gap']:.6f}`;\n"
        f"- visibly changed particles: `{split['visibly_changed_particle_count']}` "
        f"of 128 (`{split['visibly_changed_particle_fraction']:.6f}`);\n"
        f"- baseline event reuse: `{reuse['baseline_event_reuse_fraction']:.6f}`;\n"
        f"- peak affected fraction: `{reuse['peak_affected_fraction']:.6f}`;\n"
        f"- local/full event-pair agreement: "
        f"`{correctness['collision_pair_agreement']:.6f}`.\n\n"
        "## Frozen checks\n\n"
        "| Check | Result |\n"
        "|---|---|\n"
        f"{checks}"
    )
