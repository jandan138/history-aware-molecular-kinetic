from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from statistics import mean
from typing import Any

from historykinetic.e2.models import E2CaseResult, E2Direction, E2StudyResult
from historykinetic.echo.artifacts import refresh_manifest
from historykinetic.echo.models import PassiveColorMap
from historykinetic.solvers import DiskState

_COLORS = {
    "ghost": "#8b95a5",
    "budget-l4-g0": "#7a5cff",
    "budget-l8-g0": "#3958c9",
    "budget-l16-g1": "#16b9e8",
    "full": "#087e8b",
    "count-time-matched-random": "#df4f9b",
}


def render_e2(result: E2StudyResult, output_directory: Path) -> tuple[Path, Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    svg_path = output_directory / "figure-e2-main.svg"
    pdf_path = output_directory / "figure-e2-main.pdf"
    video_path = output_directory / "echo-e2-collision-wiring.mp4"
    _render_figure(result, svg_path, pdf_path)
    _render_video(result, video_path)
    manifest_path = output_directory / "render-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "render_id": "MOLECULAR-ECHOES-E2-WIRING-v0",
                "study_id": result.protocol.study_id,
                "hero_case": {
                    "particle_count": result.protocol.render.hero_particle_count,
                    "seed": result.protocol.render.hero_seed,
                },
                "comparison_lock": {
                    "camera": "fixed-orthographic-domain",
                    "timeline": "identical-physical-time",
                    "initial_state": "identical-within-direction",
                    "particle_display": "identical-across-branches",
                    "passive_colors": "inherited-from-E1",
                },
                "physics_state_mutated": False,
                "temporal_interpolation": False,
                "posthoc_particle_correction": False,
                "outputs": [svg_path.name, pdf_path.name, video_path.name],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    refresh_manifest(output_directory)
    return svg_path, pdf_path, video_path


def _render_figure(result: E2StudyResult, svg_path: Path, pdf_path: Path) -> None:
    plt = _pyplot()
    case = _hero_case(result)
    selected = result.protocol.selected_budget.branch_name
    topology = f"topology-shuffled-{selected}"
    panels = (
        ("Ghost: no collision wiring", "ghost"),
        (f"Finite molecule: {selected}", selected),
        ("Same dose, random wiring", "count-time-matched-random"),
        ("Full collision history", "full"),
    )
    figure = plt.figure(figsize=(14.0, 8.0), constrained_layout=True)
    grid = figure.add_gridspec(2, 4, height_ratios=(1.0, 1.2))
    for index, (title, branch_name) in enumerate(panels):
        axis = figure.add_subplot(grid[0, index])
        state = case.branch(E2Direction.REVERSE, branch_name).result.simulation.snapshots[-1].state
        _scatter_state(axis, state, case.colors, result, title=title)

    curve_axis = figure.add_subplot(grid[1, :2])
    curve_branches = (
        "ghost",
        *(budget.branch_name for budget in result.protocol.budgets),
        "full",
        "count-time-matched-random",
        topology,
    )
    for branch in curve_branches:
        rows_by_time: dict[float, list[float]] = {}
        for current_case in result.cases:
            for row in current_case.metrics:
                if row.direction is E2Direction.REVERSE and row.branch == branch:
                    rows_by_time.setdefault(row.time, []).append(row.color_recovery)
        times = sorted(rows_by_time)
        values = [mean(rows_by_time[time]) for time in times]
        linestyle = "--" if branch in {"count-time-matched-random", topology} else "-"
        curve_axis.plot(
            times,
            values,
            label=_short_label(branch, selected),
            color=_branch_color(branch, topology),
            linewidth=2.4 if linestyle == "-" else 1.9,
            linestyle=linestyle,
        )
    curve_axis.set_xlabel("time after mixed pivot")
    curve_axis.set_ylabel("passive-color recovery")
    curve_axis.set_title("Reverse direction: molecule budget restores the echo")
    curve_axis.grid(alpha=0.22)
    curve_axis.legend(frameon=False, fontsize=8, ncols=2)

    dose_axis = figure.add_subplot(grid[1, 2:])
    for branch in curve_branches:
        doses = [
            audit.collision_dose
            for current_case in result.cases
            for audit in current_case.audits
            if audit.direction is E2Direction.REVERSE and audit.branch == branch
        ]
        terminal_recovery = [
            row.color_recovery
            for current_case in result.cases
            for row in current_case.metrics
            if row.direction is E2Direction.REVERSE
            and row.branch == branch
            and abs(row.time - result.protocol.e1_protocol.future_horizon) <= 1.0e-12
        ]
        dose_axis.scatter(
            mean(doses),
            mean(terminal_recovery),
            color=_branch_color(branch, topology),
            marker="X" if branch in {"count-time-matched-random", topology} else "o",
            s=90,
            label=_short_label(branch, selected),
        )
    dose_axis.set_xlabel("accepted-collision dose / full dose")
    dose_axis.set_ylabel("terminal color recovery")
    dose_axis.set_title("Same dose is insufficient when collision wiring changes")
    dose_axis.grid(alpha=0.22)
    dose_axis.legend(frameon=False, fontsize=8, ncols=2)
    figure.suptitle(
        "Same present, same collision dose, different collision wiring, different future",
        fontsize=17,
        fontweight="bold",
    )
    figure.savefig(svg_path)
    figure.savefig(pdf_path)
    plt.close(figure)


def _render_video(result: E2StudyResult, video_path: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to render the E2 video")
    plt = _pyplot()
    case = _hero_case(result)
    selected = result.protocol.selected_budget.branch_name
    branches = (
        ("ghost", "Ghost"),
        (selected, "Finite collision molecule"),
        ("count-time-matched-random", "Same collision dose, random"),
        ("full", "Full collision history"),
    )
    render = result.protocol.render
    with tempfile.TemporaryDirectory(prefix="echo-e2-frames-") as temporary:
        directory = Path(temporary)
        snapshot_count = len(
            case.branch(E2Direction.REVERSE, "full").result.simulation.snapshots
        )
        frame_index = 0
        for snapshot_index in range(snapshot_count):
            frame = directory / f"frame-{frame_index:06d}.png"
            figure, axes = plt.subplots(2, 2, figsize=(12.8, 7.2))
            for axis, (branch_name, label) in zip(axes.flat, branches, strict=True):
                branch = case.branch(E2Direction.REVERSE, branch_name)
                snapshot = branch.result.simulation.snapshots[snapshot_index]
                score = next(
                    row.color_recovery
                    for row in case.metrics
                    if row.direction is E2Direction.REVERSE
                    and row.branch == branch_name
                    and abs(row.time - snapshot.time) <= 1.0e-12
                )
                _scatter_state(
                    axis,
                    snapshot.state,
                    case.colors,
                    result,
                    title=f"{label}  recovery={score:.3f}",
                )
            figure.suptitle(
                "Identical reversed pivot; only collision wiring changes",
                fontsize=17,
                fontweight="bold",
            )
            figure.savefig(frame, dpi=100)
            plt.close(figure)
            for repeat_index in range(1, render.frame_repeat):
                shutil.copyfile(
                    frame,
                    directory / f"frame-{frame_index + repeat_index:06d}.png",
                )
            frame_index += render.frame_repeat
        final_frame = directory / f"frame-{frame_index - 1:06d}.png"
        for _ in range(render.final_hold_frames):
            shutil.copyfile(final_frame, directory / f"frame-{frame_index:06d}.png")
            frame_index += 1
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-framerate",
                str(render.fps),
                "-i",
                str(directory / "frame-%06d.png"),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(video_path),
            ],
            check=True,
        )


def _scatter_state(
    axis: Any,
    state: DiskState,
    colors: PassiveColorMap,
    result: E2StudyResult,
    *,
    title: str,
) -> None:
    point_colors = [
        result.protocol.e1_protocol.render.foreground_color
        if colors.label(particle_id) == 1
        else result.protocol.e1_protocol.render.background_color
        for particle_id in state.particle_ids
    ]
    axis.scatter(
        [position[0] for position in state.positions],
        [position[1] for position in state.positions],
        s=1700.0 / state.particle_count,
        c=point_colors,
        edgecolors="none",
    )
    domain = result.protocol.e1_protocol.domain
    axis.set_xlim(domain.lower[0], domain.upper[0])
    axis.set_ylim(domain.lower[1], domain.upper[1])
    axis.set_aspect("equal", adjustable="box")
    axis.set_facecolor("#f7f8fa")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.set_title(title, fontsize=10)


def _hero_case(result: E2StudyResult) -> E2CaseResult:
    for case in result.cases:
        if (
            case.particle_count == result.protocol.render.hero_particle_count
            and case.seed == result.protocol.render.hero_seed
        ):
            return case
    raise KeyError("registered E2 hero case is missing")


def _branch_color(branch: str, topology: str) -> str:
    if branch == topology:
        return "#f1a340"
    return _COLORS[branch]


def _short_label(branch: str, selected: str) -> str:
    labels = {
        "ghost": "ghost",
        "full": "full",
        "count-time-matched-random": "dose-matched random",
        f"topology-shuffled-{selected}": "topology-shuffled",
    }
    return labels.get(branch, branch.replace("budget-", ""))


def _pyplot() -> Any:
    try:
        matplotlib = importlib.import_module("matplotlib")
        matplotlib.use("Agg")
        return importlib.import_module("matplotlib.pyplot")
    except ImportError as exc:
        raise RuntimeError("E2 rendering requires the analysis extra") from exc
