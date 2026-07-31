from __future__ import annotations

import hashlib
import importlib
import json
import random
import subprocess
from dataclasses import asdict
from pathlib import Path
from statistics import mean, median
from typing import Any

from historykinetic.echo.models import EchoMetricRow, EchoStudyResult
from historykinetic.echo.protocol import EchoBranchKind
from historykinetic.ids import content_id


def summarize_echo_e1(result: EchoStudyResult) -> dict[str, Any]:
    protocol = result.protocol
    terminal_rows = {
        (row.particle_count, row.seed, row.branch): row
        for case in result.cases
        for row in case.metrics
        if abs(row.time - protocol.future_horizon) <= 1.0e-12
    }
    pivot_rows = {
        (row.particle_count, row.seed): row
        for case in result.cases
        for row in case.metrics
        if row.branch is EchoBranchKind.EXACT_REVERSE and abs(row.time) <= 1.0e-12
    }
    gap_by_case: dict[tuple[int, int], float] = {}
    dsmc_gap_by_case: dict[tuple[int, int], float] = {}
    for case in result.cases:
        key = (case.particle_count, case.seed)
        exact = terminal_rows[(*key, EchoBranchKind.EXACT_REVERSE)].color_score
        chaos = terminal_rows[(*key, EchoBranchKind.CHAOTIZED_REVERSE)].color_score
        dsmc = terminal_rows[(*key, EchoBranchKind.DSMC_REVERSE)].color_score
        gap_by_case[key] = exact - chaos
        dsmc_gap_by_case[key] = exact - dsmc

    seed_gaps = [
        mean(gap_by_case[(size.count, seed)] for size in protocol.sizes)
        for seed in protocol.seeds
    ]
    ci_lower, ci_upper = _bootstrap_mean_interval(
        seed_gaps,
        resamples=protocol.bootstrap_resamples,
        seed=protocol.bootstrap_seed,
    )
    construction_grid = protocol.chaotization_blocks
    construction_audits = [
        audit
        for case in result.cases
        for audit in case.resolved_state_audits
        if (audit.blocks_x, audit.blocks_y) == construction_grid
    ]

    checks: dict[str, bool] = {
        "event_pair_agreement": all(
            case.reversal_audit.event_pair_agreement == 1.0 for case in result.cases
        ),
        "position_rms": all(
            case.reversal_audit.position_rms
            <= protocol.acceptance.maximum_position_rms
            for case in result.cases
        ),
        "velocity_rms": all(
            case.reversal_audit.velocity_rms
            <= protocol.acceptance.maximum_velocity_rms
            for case in result.cases
        ),
        "pivot_mixed": all(
            mean(
                pivot_rows[(size.count, seed)].color_score for seed in protocol.seeds
            )
            <= protocol.acceptance.maximum_pivot_color_score
            for size in protocol.sizes
        ),
        "exact_terminal_recovery": all(
            median(
                terminal_rows[
                    (size.count, seed, EchoBranchKind.EXACT_REVERSE)
                ].color_score
                for seed in protocol.seeds
            )
            >= protocol.acceptance.minimum_exact_terminal_color_score
            for size in protocol.sizes
        ),
        "changed_particle_fraction": all(
            case.changed_particle_fraction
            >= protocol.acceptance.minimum_changed_particle_fraction
            for case in result.cases
        ),
        "construction_tv": all(
            audit.total_variation <= protocol.acceptance.maximum_construction_tv
            for audit in construction_audits
        ),
        "invariant_mismatch": all(
            case.invariant_mismatch
            <= protocol.acceptance.maximum_invariant_mismatch
            for case in result.cases
        ),
        "mean_echo_gap": mean(gap_by_case.values())
        >= protocol.acceptance.minimum_mean_echo_gap,
        "echo_gap_ci_lower": ci_lower
        > protocol.acceptance.minimum_echo_gap_ci_lower,
        "all_echo_gaps_positive": all(gap > 0 for gap in gap_by_case.values()),
    }
    kinetic_support = all(gap > 0 for gap in dsmc_gap_by_case.values())
    core_pass = all(checks.values())
    if not core_pass:
        decision = "stop_e1"
    elif kinetic_support:
        decision = "go"
    else:
        decision = "narrow"

    by_size = {}
    for size in protocol.sizes:
        count = size.count
        size_cases = [case for case in result.cases if case.particle_count == count]
        by_size[str(count)] = {
            "pivot_color_score_mean": mean(
                pivot_rows[(count, seed)].color_score for seed in protocol.seeds
            ),
            "exact_terminal_color_score_median": median(
                terminal_rows[(count, seed, EchoBranchKind.EXACT_REVERSE)].color_score
                for seed in protocol.seeds
            ),
            "chaotized_terminal_color_score_mean": mean(
                terminal_rows[
                    (count, seed, EchoBranchKind.CHAOTIZED_REVERSE)
                ].color_score
                for seed in protocol.seeds
            ),
            "dsmc_terminal_color_score_mean": mean(
                terminal_rows[(count, seed, EchoBranchKind.DSMC_REVERSE)].color_score
                for seed in protocol.seeds
            ),
            "echo_gap_mean": mean(
                gap_by_case[(count, seed)] for seed in protocol.seeds
            ),
            "maximum_position_rms": max(
                case.reversal_audit.position_rms for case in size_cases
            ),
            "maximum_velocity_rms": max(
                case.reversal_audit.velocity_rms for case in size_cases
            ),
            "minimum_changed_particle_fraction": min(
                case.changed_particle_fraction for case in size_cases
            ),
        }

    return {
        "schema_version": "1.0.0",
        "study_id": protocol.study_id,
        "decision": decision,
        "core_pass": core_pass,
        "kinetic_support": kinetic_support,
        "checks": checks,
        "combined": {
            "echo_gap_mean": mean(gap_by_case.values()),
            "echo_gap_seed_bootstrap_95_ci": [ci_lower, ci_upper],
            "minimum_echo_gap": min(gap_by_case.values()),
            "maximum_echo_gap": max(gap_by_case.values()),
        },
        "by_particle_count": by_size,
    }


def write_echo_e1_result(
    result: EchoStudyResult,
    output_directory: Path,
    *,
    protocol_path: Path,
    include_trajectories: bool = True,
) -> dict[str, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    metrics_path = output_directory / "branch-metrics.jsonl"
    metrics_text = "".join(
        json.dumps(_metric_payload(row), sort_keys=True, separators=(",", ":")) + "\n"
        for case in result.cases
        for row in case.metrics
    )
    metrics_path.write_text(metrics_text, encoding="utf-8")
    paths["metrics"] = metrics_path

    reversal_path = output_directory / "reversal-audit.json"
    reversal_path.write_text(
        json.dumps(
            [asdict(case.reversal_audit) for case in result.cases],
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["reversal_audit"] = reversal_path

    pivot_path = output_directory / "pivot-audit.json"
    pivot_path.write_text(
        json.dumps(
            {
                "resolved_state_audits": [
                    asdict(audit)
                    for case in result.cases
                    for audit in case.resolved_state_audits
                ],
                "changed_particle_fraction": [
                    {
                        "particle_count": case.particle_count,
                        "seed": case.seed,
                        "value": case.changed_particle_fraction,
                    }
                    for case in result.cases
                ],
                "invariant_mismatch": [
                    {
                        "particle_count": case.particle_count,
                        "seed": case.seed,
                        "value": case.invariant_mismatch,
                    }
                    for case in result.cases
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["pivot_audit"] = pivot_path

    summary = summarize_echo_e1(result)
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
        trajectories_path = output_directory / "particle-trajectories.npz"
        _write_trajectories(result, trajectories_path)
        paths["trajectories"] = trajectories_path

    manifest_path = output_directory / "run-manifest.json"
    manifest = {
        "schema_version": "1.0.0",
        "study_id": result.protocol.study_id,
        "study_content_id": content_id("echo-e1", asdict(result.protocol)),
        "protocol": {
            "path": protocol_path.as_posix(),
            "sha256": _sha256(protocol_path),
        },
        "repository": _repository_state(),
        "cases": [
            {
                "particle_count": case.particle_count,
                "seed": case.seed,
                "branches": [branch.kind.value for branch in case.branches],
            }
            for case in result.cases
        ],
        "artifacts": {},
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths["manifest"] = manifest_path
    refresh_manifest(output_directory)
    return paths


def refresh_manifest(output_directory: Path) -> Path:
    manifest_path = output_directory / "run-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifacts = {}
    for path in sorted(output_directory.iterdir()):
        if not path.is_file() or path == manifest_path:
            continue
        artifacts[path.name] = {
            "sha256": _sha256(path),
            "bytes": path.stat().st_size,
        }
    manifest["artifacts"] = artifacts
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def _metric_payload(row: EchoMetricRow) -> dict[str, Any]:
    return {
        "particle_count": row.particle_count,
        "seed": row.seed,
        "branch": row.branch.value,
        "time": row.time,
        "color_score": row.color_score,
        "color_recovery": row.color_recovery,
        "anisotropy": row.anisotropy,
    }


def _bootstrap_mean_interval(
    values: list[float],
    *,
    resamples: int,
    seed: int,
) -> tuple[float, float]:
    if not values or resamples < 100:
        raise ValueError("bootstrap requires values and at least 100 resamples")
    rng = random.Random(seed)
    samples = sorted(
        mean(rng.choice(values) for _ in values) for _ in range(resamples)
    )
    return (
        _quantile(samples, 0.025),
        _quantile(samples, 0.975),
    )


def _quantile(values: list[float], probability: float) -> float:
    position = probability * (len(values) - 1)
    lower = int(position)
    upper = min(len(values) - 1, lower + 1)
    fraction = position - lower
    return values[lower] * (1.0 - fraction) + values[upper] * fraction


def _write_trajectories(result: EchoStudyResult, path: Path) -> None:
    try:
        np = importlib.import_module("numpy")
    except ImportError as exc:
        raise RuntimeError("trajectory output requires the analysis extra") from exc

    arrays: dict[str, Any] = {}
    for case in result.cases:
        prefix = f"n{case.particle_count}_seed{case.seed}"
        arrays[f"{prefix}_colors"] = np.asarray(
            case.colors.labels_by_particle_id, dtype=np.int8
        )
        arrays[f"{prefix}_preparation_positions"] = np.asarray(
            [snapshot.state.positions for snapshot in case.preparation.snapshots],
            dtype=np.float64,
        )
        arrays[f"{prefix}_preparation_velocities"] = np.asarray(
            [snapshot.state.velocities for snapshot in case.preparation.snapshots],
            dtype=np.float64,
        )
        for branch in case.branches:
            branch_prefix = f"{prefix}_{branch.kind.value}"
            arrays[f"{branch_prefix}_positions"] = np.asarray(
                [snapshot.state.positions for snapshot in branch.result.snapshots],
                dtype=np.float64,
            )
            arrays[f"{branch_prefix}_velocities"] = np.asarray(
                [snapshot.state.velocities for snapshot in branch.result.snapshots],
                dtype=np.float64,
            )
    np.savez_compressed(path, **arrays)


def _repository_state() -> dict[str, Any]:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return {
        "commit": commit,
        "dirty": bool(status.strip()),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _decision_markdown(summary: dict[str, Any]) -> str:
    checks = summary["checks"]
    rows = "\n".join(
        f"| {name} | {'PASS' if passed else 'FAIL'} |"
        for name, passed in checks.items()
    )
    combined = summary["combined"]
    return (
        "# Molecular Echoes E1 decision\n\n"
        f"**Decision:** `{summary['decision']}`\n\n"
        "## Story result\n\n"
        f"- mean exact-chaotized terminal color gap: "
        f"`{combined['echo_gap_mean']:.6f}`;\n"
        f"- seed-bootstrap 95% interval: "
        f"`[{combined['echo_gap_seed_bootstrap_95_ci'][0]:.6f}, "
        f"{combined['echo_gap_seed_bootstrap_95_ci'][1]:.6f}]`;\n"
        f"- DSMC supports the scoped kinetic interpretation: "
        f"`{str(summary['kinetic_support']).lower()}`.\n\n"
        "## Frozen checks\n\n"
        "| Check | Result |\n"
        "|---|---|\n"
        f"{rows}\n\n"
        "The claim is restricted to the preregistered 4x2 resolved state. "
        "Finer-grid audits are disclosures, not claims of continuous-f1 equality."
    )
