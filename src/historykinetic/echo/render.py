from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from statistics import mean
from typing import Any

from historykinetic.echo.artifacts import refresh_manifest
from historykinetic.echo.models import EchoCaseResult, EchoStudyResult, PassiveColorMap
from historykinetic.echo.protocol import EchoBranchKind
from historykinetic.solvers import DiskState

_BRANCH_COLORS = {
    EchoBranchKind.FORWARD: "#8b95a5",
    EchoBranchKind.EXACT_REVERSE: "#16b9e8",
    EchoBranchKind.CHAOTIZED_REVERSE: "#df4f9b",
    EchoBranchKind.DSMC_REVERSE: "#f1a340",
}


def render_echo_e1(
    result: EchoStudyResult,
    output_directory: Path,
) -> tuple[Path, Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_svg = output_directory / "figure-e1-main.svg"
    figure_pdf = output_directory / "figure-e1-main.pdf"
    video = output_directory / "echo-e1-neutral.mp4"
    _render_main_figure(result, figure_svg, figure_pdf)
    _render_neutral_video(result, video)
    render_manifest = output_directory / "render-manifest.json"
    render_manifest.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "render_id": "MOLECULAR-ECHOES-E1-NEUTRAL-v0",
                "study_id": result.protocol.study_id,
                "hero_case": {
                    "particle_count": result.protocol.render.hero_particle_count,
                    "seed": result.protocol.render.hero_seed,
                },
                "comparison_lock": {
                    "domain": [
                        list(result.protocol.domain.lower),
                        list(result.protocol.domain.upper),
                    ],
                    "timeline": {
                        "preparation_time": result.protocol.preparation_time,
                        "future_horizon": result.protocol.future_horizon,
                        "sample_interval": result.protocol.sample_interval,
                    },
                    "camera": "fixed-orthographic-domain",
                    "particle_display": "identical-across-branches",
                    "passive_colors": [
                        result.protocol.render.background_color,
                        result.protocol.render.foreground_color,
                    ],
                },
                "physics_state_mutated": False,
                "temporal_interpolation": False,
                "video_reversal": False,
                "posthoc_particle_correction": False,
                "outputs": [figure_svg.name, figure_pdf.name, video.name],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    refresh_manifest(output_directory)
    return figure_svg, figure_pdf, video


def _render_main_figure(
    result: EchoStudyResult,
    svg_path: Path,
    pdf_path: Path,
) -> None:
    plt = _pyplot()
    case = _hero_case(result)
    exact_terminal = case.branch(EchoBranchKind.EXACT_REVERSE).result.snapshots[-1].state
    chaos_terminal = case.branch(
        EchoBranchKind.CHAOTIZED_REVERSE
    ).result.snapshots[-1].state
    figure = plt.figure(figsize=(13.5, 7.4), constrained_layout=True)
    grid = figure.add_gridspec(2, 4, height_ratios=(1.0, 1.15))
    snapshot_specs = (
        ("Initial color E", case.initial_state),
        ("Mixed pivot", case.preparation.snapshots[-1].state),
        ("Exact reverse", exact_terminal),
        ("Chaotized reverse", chaos_terminal),
    )
    for index, (title, state) in enumerate(snapshot_specs):
        axis = figure.add_subplot(grid[0, index])
        _scatter_state(
            axis,
            state,
            case.colors,
            result,
            title=title,
        )

    curve_axis = figure.add_subplot(grid[1, :])
    for kind in (
        EchoBranchKind.FORWARD,
        EchoBranchKind.EXACT_REVERSE,
        EchoBranchKind.CHAOTIZED_REVERSE,
        EchoBranchKind.DSMC_REVERSE,
    ):
        rows_by_time: dict[float, list[float]] = {}
        for current_case in result.cases:
            for row in current_case.metrics:
                if row.branch is kind:
                    rows_by_time.setdefault(row.time, []).append(row.color_score)
        times = sorted(rows_by_time)
        means = [mean(rows_by_time[time]) for time in times]
        lows = [min(rows_by_time[time]) for time in times]
        highs = [max(rows_by_time[time]) for time in times]
        label = {
            EchoBranchKind.FORWARD: "forward",
            EchoBranchKind.EXACT_REVERSE: "exact reverse",
            EchoBranchKind.CHAOTIZED_REVERSE: "chaotized reverse",
            EchoBranchKind.DSMC_REVERSE: "DSMC (supporting)",
        }[kind]
        curve_axis.plot(
            times,
            means,
            color=_BRANCH_COLORS[kind],
            linewidth=2.8 if kind is not EchoBranchKind.DSMC_REVERSE else 1.8,
            label=label,
        )
        curve_axis.fill_between(
            times,
            lows,
            highs,
            color=_BRANCH_COLORS[kind],
            alpha=0.10,
            linewidth=0,
        )
    construction_audit = next(
        audit
        for audit in case.resolved_state_audits
        if (audit.blocks_x, audit.blocks_y) == result.protocol.chaotization_blocks
        and audit.velocity_bin_count == 8
    )
    curve_axis.text(
        0.015,
        0.04,
        f"pivot audit: 4x2 resolved f1,h TV = {construction_audit.total_variation:.1e}",
        transform=curve_axis.transAxes,
        fontsize=10,
        bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "#c9ced6"},
    )
    curve_axis.set_xlabel("time after pivot")
    curve_axis.set_ylabel("passive-color E score")
    curve_axis.set_xlim(0.0, result.protocol.future_horizon)
    curve_axis.set_ylim(0.35, 1.02)
    curve_axis.grid(alpha=0.22)
    curve_axis.legend(loc="upper left", ncols=4, frameon=False)
    figure.suptitle(
        "Same resolved present, opposite futures",
        fontsize=17,
        fontweight="bold",
    )
    figure.savefig(svg_path)
    figure.savefig(pdf_path)
    plt.close(figure)


def _render_neutral_video(result: EchoStudyResult, video_path: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to render the neutral E1 video")
    plt = _pyplot()
    case = _hero_case(result)
    render = result.protocol.render
    with tempfile.TemporaryDirectory(prefix="echo-e1-frames-") as temporary:
        directory = Path(temporary)
        frame_index = 0
        last_frame: Path | None = None
        for snapshot in case.preparation.snapshots:
            frame = directory / f"frame-{frame_index:06d}.png"
            figure, axis = plt.subplots(figsize=(12.8, 7.2))
            _scatter_state(
                axis,
                snapshot.state,
                case.colors,
                result,
                title=f"Shared preparation  t={snapshot.time:.2f}",
            )
            figure.suptitle(
                "A passive-color E disperses before the pivot",
                fontsize=18,
                fontweight="bold",
            )
            figure.savefig(frame, dpi=100)
            plt.close(figure)
            frame_index = _repeat_frame(
                frame,
                directory,
                frame_index,
                render.frame_repeat,
            )
            last_frame = directory / f"frame-{frame_index - 1:06d}.png"

        if last_frame is None:
            raise AssertionError("preparation produced no video frames")
        for _ in range(render.fps):
            target = directory / f"frame-{frame_index:06d}.png"
            shutil.copyfile(last_frame, target)
            frame_index += 1

        branch_kinds = (
            EchoBranchKind.FORWARD,
            EchoBranchKind.EXACT_REVERSE,
            EchoBranchKind.CHAOTIZED_REVERSE,
            EchoBranchKind.DSMC_REVERSE,
        )
        snapshot_count = len(case.branch(EchoBranchKind.FORWARD).result.snapshots)
        for snapshot_index in range(snapshot_count):
            frame = directory / f"frame-{frame_index:06d}.png"
            figure, axes = plt.subplots(2, 2, figsize=(12.8, 7.2))
            for axis, kind in zip(axes.flat, branch_kinds, strict=True):
                branch = case.branch(kind)
                snapshot = branch.result.snapshots[snapshot_index]
                score = next(
                    row.color_score
                    for row in case.metrics
                    if row.branch is kind and abs(row.time - snapshot.time) <= 1.0e-12
                )
                _scatter_state(
                    axis,
                    snapshot.state,
                    case.colors,
                    result,
                    title=f"{kind.value.replace('_', ' ')}  score={score:.3f}",
                )
            figure.suptitle(
                "Same 4x2 resolved pivot; four forward-simulated futures",
                fontsize=17,
                fontweight="bold",
            )
            figure.savefig(frame, dpi=100)
            plt.close(figure)
            frame_index = _repeat_frame(
                frame,
                directory,
                frame_index,
                render.frame_repeat,
            )
            last_frame = directory / f"frame-{frame_index - 1:06d}.png"

        if last_frame is None:
            raise AssertionError("branch phase produced no video frames")
        for _ in range(render.final_hold_frames):
            target = directory / f"frame-{frame_index:06d}.png"
            shutil.copyfile(last_frame, target)
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


def _repeat_frame(
    rendered_frame: Path,
    directory: Path,
    frame_index: int,
    repeat: int,
) -> int:
    original_index = frame_index
    frame_index += 1
    for _ in range(1, repeat):
        target = directory / f"frame-{frame_index:06d}.png"
        source = directory / f"frame-{original_index:06d}.png"
        shutil.copyfile(source, target)
        frame_index += 1
    return frame_index


def _scatter_state(
    axis: Any,
    state: DiskState,
    colors: PassiveColorMap,
    result: EchoStudyResult,
    *,
    title: str,
) -> None:
    foreground = result.protocol.render.foreground_color
    background = result.protocol.render.background_color
    point_colors = [
        foreground if colors.label(particle_id) == 1 else background
        for particle_id in state.particle_ids
    ]
    marker_size = 1700.0 / state.particle_count
    axis.scatter(
        [position[0] for position in state.positions],
        [position[1] for position in state.positions],
        s=marker_size,
        c=point_colors,
        edgecolors="none",
    )
    axis.set_xlim(result.protocol.domain.lower[0], result.protocol.domain.upper[0])
    axis.set_ylim(result.protocol.domain.lower[1], result.protocol.domain.upper[1])
    axis.set_aspect("equal", adjustable="box")
    axis.set_facecolor("#f7f8fa")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.set_title(title, fontsize=11)


def _hero_case(result: EchoStudyResult) -> EchoCaseResult:
    for case in result.cases:
        if (
            case.particle_count == result.protocol.render.hero_particle_count
            and case.seed == result.protocol.render.hero_seed
        ):
            return case
    raise KeyError("registered hero case is missing from the E1 result")


def _pyplot() -> Any:
    try:
        matplotlib = importlib.import_module("matplotlib")
        matplotlib.use("Agg")
        pyplot = importlib.import_module("matplotlib.pyplot")
    except ImportError as exc:
        raise RuntimeError("E1 rendering requires the analysis extra") from exc
    return pyplot
