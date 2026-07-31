from __future__ import annotations

import gzip
import hashlib
import importlib
import json
import random
import subprocess
from dataclasses import asdict
from math import sqrt
from pathlib import Path
from statistics import mean
from typing import Any

from historykinetic.e2.models import E2Direction, E2MetricRow, E2StudyResult
from historykinetic.echo.artifacts import refresh_manifest
from historykinetic.ids import content_id


def summarize_e2(result: E2StudyResult) -> dict[str, Any]:
    protocol = result.protocol
    horizon = protocol.e1_protocol.future_horizon
    terminal = {
        (row.particle_count, row.seed, row.direction, row.branch): row
        for case in result.cases
        for row in case.metrics
        if abs(row.time - horizon) <= 1.0e-12
    }
    audit = {
        (row.particle_count, row.seed, row.direction, row.branch): row
        for case in result.cases
        for row in case.audits
    }
    ladder = (
        "ghost",
        *(budget.branch_name for budget in protocol.budgets),
        "full",
    )
    selected = protocol.selected_budget.branch_name
    topology = f"topology-shuffled-{selected}"
    case_keys = [
        (case.particle_count, case.seed)
        for case in result.cases
    ]
    reverse_rhos = [
        _spearman(
            [
                terminal[(*key, E2Direction.REVERSE, branch)].color_recovery
                for branch in ladder
            ]
        )
        for key in case_keys
    ]
    full_ghost_gaps = [
        terminal[(*key, E2Direction.REVERSE, "full")].color_score
        - terminal[(*key, E2Direction.REVERSE, "ghost")].color_score
        for key in case_keys
    ]
    random_gaps = {
        key: terminal[(*key, E2Direction.REVERSE, selected)].color_score
        - terminal[
            (*key, E2Direction.REVERSE, "count-time-matched-random")
        ].color_score
        for key in case_keys
    }
    topology_gaps = {
        key: terminal[(*key, E2Direction.REVERSE, selected)].color_score
        - terminal[(*key, E2Direction.REVERSE, topology)].color_score
        for key in case_keys
    }
    random_seed_gaps = [
        mean(random_gaps[(size.count, seed)] for size in protocol.e1_protocol.sizes)
        for seed in protocol.seeds
    ]
    topology_seed_gaps = [
        mean(topology_gaps[(size.count, seed)] for size in protocol.e1_protocol.sizes)
        for seed in protocol.seeds
    ]
    random_ci = _bootstrap_mean_interval(
        random_seed_gaps,
        resamples=protocol.bootstrap_resamples,
        seed=protocol.bootstrap_seed,
    )
    topology_ci = _bootstrap_mean_interval(
        topology_seed_gaps,
        resamples=protocol.bootstrap_resamples,
        seed=protocol.bootstrap_seed + 1,
    )
    dose_errors = []
    for key in case_keys:
        for direction in E2Direction:
            target_dose = audit[(*key, direction, selected)].collision_dose
            for control in ("count-time-matched-random", topology):
                control_dose = audit[(*key, direction, control)].collision_dose
                dose_errors.append(
                    abs(control_dose - target_dose) / max(target_dose, 1.0e-15)
                )
    forward_mean_recovery = {
        branch: mean(
            terminal[(*key, E2Direction.FORWARD, branch)].color_recovery
            for key in case_keys
        )
        for branch in ladder
    }
    checks = {
        "reverse_budget_ladder": mean(reverse_rhos)
        >= protocol.acceptance.minimum_reverse_ladder_spearman,
        "reverse_full_ghost_separation": mean(full_ghost_gaps)
        >= protocol.acceptance.minimum_reverse_full_ghost_gap,
        "structured_beats_random": mean(random_gaps.values())
        >= protocol.acceptance.minimum_selected_random_gap,
        "structured_beats_topology_shuffle": mean(topology_gaps.values())
        >= protocol.acceptance.minimum_selected_topology_gap,
        "random_gap_ci": random_ci[0]
        > protocol.acceptance.minimum_control_gap_ci_lower,
        "topology_gap_ci": topology_ci[0]
        > protocol.acceptance.minimum_control_gap_ci_lower,
        "control_collision_dose": max(dose_errors)
        <= protocol.acceptance.maximum_control_dose_relative_error,
        "no_forward_echo": max(forward_mean_recovery.values())
        <= protocol.acceptance.maximum_forward_recovery,
        "conservation": all(
            branch.result.simulation.diagnostics.relative_energy_error <= 1.0e-12
            and branch.result.simulation.diagnostics.absolute_momentum_error <= 1.0e-12
            for case in result.cases
            for branch in case.branches
        ),
    }
    if all(checks.values()):
        decision = "go"
    elif (
        checks["reverse_budget_ladder"]
        and checks["reverse_full_ghost_separation"]
        and (checks["structured_beats_random"] or checks["structured_beats_topology_shuffle"])
    ):
        decision = "narrow"
    else:
        decision = "stop_e2"

    by_branch: dict[str, Any] = {}
    for direction in E2Direction:
        by_branch[direction.value] = {}
        for branch in protocol.branch_names:
            rows = [
                terminal[(*key, direction, branch)]
                for key in case_keys
            ]
            audits = [audit[(*key, direction, branch)] for key in case_keys]
            by_branch[direction.value][branch] = {
                "terminal_color_score_mean": mean(row.color_score for row in rows),
                "terminal_color_recovery_mean": mean(
                    row.color_recovery for row in rows
                ),
                "collision_dose_mean": mean(row.collision_dose for row in audits),
                "incoming_pair_closure_defect_mean": mean(
                    row.incoming_pair_closure_defect for row in audits
                ),
                "mirrored_pair_alignment_mean": mean(
                    row.mirrored_pair_alignment for row in audits
                ),
            }
    return {
        "schema_version": "1.0.0",
        "study_id": protocol.study_id,
        "decision": decision,
        "checks": checks,
        "selected_control_budget": selected,
        "combined": {
            "reverse_ladder_spearman_mean": mean(reverse_rhos),
            "reverse_full_ghost_color_gap_mean": mean(full_ghost_gaps),
            "selected_minus_random_color_gap_mean": mean(random_gaps.values()),
            "selected_minus_random_seed_bootstrap_95_ci": list(random_ci),
            "selected_minus_topology_color_gap_mean": mean(topology_gaps.values()),
            "selected_minus_topology_seed_bootstrap_95_ci": list(topology_ci),
            "maximum_control_dose_relative_error": max(dose_errors),
            "maximum_forward_mean_color_recovery": max(
                forward_mean_recovery.values()
            ),
        },
        "by_direction_and_branch": by_branch,
    }


def write_e2_result(
    result: E2StudyResult,
    output_directory: Path,
    *,
    protocol_path: Path,
    calibration_path: Path,
    include_trajectories: bool = True,
) -> dict[str, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    metrics_path = output_directory / "branch-metrics.jsonl"
    metrics_path.write_text(
        "".join(
            json.dumps(_metric_payload(row), sort_keys=True, separators=(",", ":"))
            + "\n"
            for case in result.cases
            for row in case.metrics
        ),
        encoding="utf-8",
    )
    paths["metrics"] = metrics_path
    audit_path = output_directory / "mechanism-audit.jsonl"
    audit_path.write_text(
        "".join(
            json.dumps(
                {
                    **asdict(row),
                    "direction": row.direction.value,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
            for case in result.cases
            for row in case.audits
        ),
        encoding="utf-8",
    )
    paths["audit"] = audit_path
    events_path = output_directory / "encounter-events.jsonl.gz"
    with gzip.open(events_path, "wt", encoding="utf-8") as handle:
        for case in result.cases:
            for branch in case.branches:
                for event in branch.result.encounter_events:
                    handle.write(
                        json.dumps(
                            {
                                "particle_count": case.particle_count,
                                "seed": case.seed,
                                "direction": branch.direction.value,
                                "branch": branch.name,
                                **asdict(event),
                                "decision": event.decision.value,
                            },
                            sort_keys=True,
                            separators=(",", ":"),
                        )
                        + "\n"
                    )
    paths["events"] = events_path
    summary = summarize_e2(result)
    summary_path = output_directory / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    paths["summary"] = summary_path
    decision_path = output_directory / "decision.md"
    decision_path.write_text(_decision_markdown(summary) + "\n", encoding="utf-8")
    paths["decision"] = decision_path
    if include_trajectories:
        trajectory_path = output_directory / "particle-trajectories.npz"
        _write_trajectories(result, trajectory_path)
        paths["trajectories"] = trajectory_path

    manifest_path = output_directory / "run-manifest.json"
    manifest = {
        "schema_version": "1.0.0",
        "study_id": result.protocol.study_id,
        "study_content_id": content_id("echo-e2", asdict(result.protocol)),
        "protocol": {"path": protocol_path.as_posix(), "sha256": _sha256(protocol_path)},
        "e1_protocol": {
            "path": result.protocol.e1_protocol_path.as_posix(),
            "sha256": _sha256(result.protocol.e1_protocol_path),
        },
        "excluded_calibration": {
            "path": calibration_path.as_posix(),
            "sha256": _sha256(calibration_path),
        },
        "repository": _repository_state(),
        "cases": [
            {"particle_count": case.particle_count, "seed": case.seed}
            for case in result.cases
        ],
        "artifacts": {},
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    paths["manifest"] = manifest_path
    refresh_manifest(output_directory)
    return paths


def _metric_payload(row: E2MetricRow) -> dict[str, Any]:
    return {
        **asdict(row),
        "direction": row.direction.value,
    }


def _spearman(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    ranks = _average_ranks(values)
    x_mean = (len(values) - 1) / 2
    y_mean = mean(ranks)
    numerator = sum((index - x_mean) * (rank - y_mean) for index, rank in enumerate(ranks))
    denominator_x = sum((index - x_mean) ** 2 for index in range(len(values)))
    denominator_y = sum((rank - y_mean) ** 2 for rank in ranks)
    if denominator_x <= 0 or denominator_y <= 0:
        return 0.0
    return numerator / sqrt(denominator_x * denominator_y)


def _average_ranks(values: list[float]) -> list[float]:
    sorted_pairs = sorted((value, index) for index, value in enumerate(values))
    ranks = [0.0] * len(values)
    cursor = 0
    while cursor < len(sorted_pairs):
        end = cursor + 1
        while end < len(sorted_pairs) and sorted_pairs[end][0] == sorted_pairs[cursor][0]:
            end += 1
        rank = 0.5 * (cursor + end - 1)
        for _, original_index in sorted_pairs[cursor:end]:
            ranks[original_index] = rank
        cursor = end
    return ranks


def _bootstrap_mean_interval(
    values: list[float],
    *,
    resamples: int,
    seed: int,
) -> tuple[float, float]:
    rng = random.Random(seed)
    samples = sorted(mean(rng.choice(values) for _ in values) for _ in range(resamples))
    return (_quantile(samples, 0.025), _quantile(samples, 0.975))


def _quantile(values: list[float], probability: float) -> float:
    position = probability * (len(values) - 1)
    lower = int(position)
    upper = min(len(values) - 1, lower + 1)
    fraction = position - lower
    return values[lower] * (1.0 - fraction) + values[upper] * fraction


def _write_trajectories(result: E2StudyResult, path: Path) -> None:
    try:
        np = importlib.import_module("numpy")
    except ImportError as exc:
        raise RuntimeError("E2 trajectory output requires the analysis extra") from exc
    arrays: dict[str, Any] = {}
    for case in result.cases:
        prefix = f"n{case.particle_count}_seed{case.seed}"
        arrays[f"{prefix}_colors"] = np.asarray(
            case.colors.labels_by_particle_id, dtype=np.int8
        )
        for branch in case.branches:
            branch_prefix = f"{prefix}_{branch.direction.value}_{branch.name}"
            arrays[f"{branch_prefix}_positions"] = np.asarray(
                [snapshot.state.positions for snapshot in branch.result.simulation.snapshots],
                dtype=np.float64,
            )
    np.savez_compressed(path, **arrays)


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
    combined = summary["combined"]
    checks = "\n".join(
        f"| {name} | {'PASS' if value else 'FAIL'} |"
        for name, value in summary["checks"].items()
    )
    return (
        "# Molecular Echoes E2 decision\n\n"
        f"**Decision:** `{summary['decision']}`\n\n"
        "## Story result\n\n"
        f"- selected finite molecule: `{summary['selected_control_budget']}`;\n"
        f"- reverse budget-ladder Spearman: "
        f"`{combined['reverse_ladder_spearman_mean']:.6f}`;\n"
        f"- selected minus count/time-matched random: "
        f"`{combined['selected_minus_random_color_gap_mean']:.6f}` "
        f"(95% CI `{combined['selected_minus_random_seed_bootstrap_95_ci']}`);\n"
        f"- selected minus topology-shuffled: "
        f"`{combined['selected_minus_topology_color_gap_mean']:.6f}` "
        f"(95% CI `{combined['selected_minus_topology_seed_bootstrap_95_ci']}`).\n\n"
        "## Preregistered checks\n\n"
        "| Check | Result |\n|---|---|\n"
        f"{checks}\n"
    )
