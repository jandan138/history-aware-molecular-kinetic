from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import tempfile
from math import cos, radians, sin
from pathlib import Path
from typing import Any

from historykinetic.echo.artifacts import refresh_manifest
from historykinetic.solvers import DiskState
from historykinetic.timeline import CollisionCausalGraph

from .models import MolecularTimeMachineE3Result


def render_molecular_time_machine_e3(
    result: MolecularTimeMachineE3Result,
    output_directory: Path,
) -> tuple[Path, Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    svg_path = output_directory / "figure-one-collision-two-worlds.svg"
    pdf_path = output_directory / "figure-one-collision-two-worlds.pdf"
    video_path = output_directory / "one-collision-two-worlds.mp4"
    _render_figure(result, svg_path, pdf_path)
    _render_video(result, video_path)
    manifest_path = output_directory / "render-manifest.json"
    render = result.protocol.render
    frame_count = len(result.timeline.result.snapshots) * render.frame_repeat
    duration = (frame_count + render.final_hold_frames) / render.fps
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "render_id": "ONE-COLLISION-TWO-WORLDS-v0",
                "study_id": result.protocol.study_id,
                "hero": {
                    "target_event_id": result.target_event.event_id,
                    "target_pair": list(result.target_event.pair),
                    "edit_angle_degrees": result.protocol.edit_angle_degrees,
                },
                "comparison_lock": {
                    "camera": "fixed-orthographic-domain",
                    "timeline": "identical-physical-time",
                    "particle_display": "identical-across-worlds",
                    "passive_colors": "inherited-from-E1",
                },
                "physics_edit_applied_by_simulator": True,
                "renderer_mutates_physics_state": False,
                "temporal_interpolation": False,
                "posthoc_particle_correction": False,
                "video_duration_seconds": duration,
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


def _render_figure(
    result: MolecularTimeMachineE3Result,
    svg_path: Path,
    pdf_path: Path,
) -> None:
    plt = _pyplot()
    figure = plt.figure(figsize=(15.5, 8.6), constrained_layout=True)
    grid = figure.add_gridspec(2, 3, height_ratios=(0.82, 1.18))

    pivot_axis = figure.add_subplot(grid[0, 0])
    _scatter_state(
        pivot_axis,
        result.fork_checkpoint.state,
        result,
        title="1  Rewind to collision #2",
        outlined=set(result.target_event.pair),
        outline_color=result.protocol.render.edited_highlight_color,
    )
    target_positions = [
        result.fork_checkpoint.state.positions[
            result.fork_checkpoint.state.particle_ids.index(particle_id)
        ]
        for particle_id in result.target_event.pair
    ]
    target_midpoint = (
        sum(position[0] for position in target_positions) / 2.0,
        sum(position[1] for position in target_positions) / 2.0,
    )
    pivot_axis.annotate(
        "pair 101-118",
        xy=target_midpoint,
        xytext=(target_midpoint[0] + 0.55, target_midpoint[1] + 0.35),
        arrowprops={"arrowstyle": "->", "color": "#ff4f87", "linewidth": 1.4},
        color="#ff4f87",
        fontsize=9,
        fontweight="bold",
    )

    timeline_axis = figure.add_subplot(grid[0, 1])
    graph = CollisionCausalGraph(result.timeline.events)
    descendants = {
        result.target_event.event_id,
        *(event.event_id for event in graph.descendants(result.target_event.event_id)),
    }
    timeline_axis.scatter(
        [event.time for event in result.timeline.events],
        [0.0] * len(result.timeline.events),
        s=14,
        color="#aab2bf",
        alpha=0.45,
    )
    timeline_axis.scatter(
        [event.time for event in result.timeline.events if event.event_id in descendants],
        [0.0 for event in result.timeline.events if event.event_id in descendants],
        s=22,
        color=result.protocol.render.causal_cone_color,
        alpha=0.82,
        label="baseline causal descendants",
    )
    timeline_axis.scatter(
        [result.target_event.time],
        [0.0],
        s=120,
        marker="*",
        color=result.protocol.render.edited_highlight_color,
        zorder=5,
        label="selected collision #2",
    )
    timeline_axis.axvline(result.target_event.time, color="#ff4f87", linewidth=1.2)
    timeline_axis.set_xlim(0.0, result.protocol.end_time)
    timeline_axis.set_ylim(-0.12, 0.12)
    timeline_axis.set_yticks([])
    timeline_axis.set_xlabel("time")
    timeline_axis.set_title("2  Every collision has an address")
    timeline_axis.legend(frameon=False, fontsize=8, loc="upper right")

    edit_axis = figure.add_subplot(grid[0, 2])
    angle = radians(result.protocol.edit_angle_degrees)
    edit_axis.arrow(
        0.0,
        0.0,
        1.0,
        0.0,
        width=0.012,
        head_width=0.11,
        length_includes_head=True,
        color="#8b95a5",
    )
    edit_axis.arrow(
        0.0,
        0.0,
        cos(angle),
        sin(angle),
        width=0.012,
        head_width=0.11,
        length_includes_head=True,
        color=result.protocol.render.edited_highlight_color,
    )
    edit_axis.text(0.47, 0.14, "+1°", color="#ff4f87", fontsize=18, fontweight="bold")
    edit_axis.text(
        0.0,
        -0.28,
        "relative velocity in pair COM frame\npositions, momentum, and energy preserved",
        fontsize=9,
    )
    edit_axis.set_xlim(-0.08, 1.15)
    edit_axis.set_ylim(-0.38, 0.38)
    edit_axis.set_aspect("equal")
    edit_axis.axis("off")
    edit_axis.set_title("3  Make one physical edit")

    baseline_axis = figure.add_subplot(grid[1, 0])
    _scatter_state(
        baseline_axis,
        result.timeline.result.snapshots[-1].state,
        result,
        title=f"Original world  E-score={result.metrics.baseline_terminal_color_score:.3f}",
    )
    edited_axis = figure.add_subplot(grid[1, 1])
    _scatter_state(
        edited_axis,
        result.branch.local.simulation.snapshots[-1].state,
        result,
        title=f"Edited world  E-score={result.metrics.edited_terminal_color_score:.3f}",
    )
    cone_axis = figure.add_subplot(grid[1, 2])
    _scatter_state(
        cone_axis,
        result.branch.local.simulation.snapshots[-1].state,
        result,
        title=(
            f"Causal cone: {len(result.branch.local.affected_particle_ids)}/"
            f"{result.protocol.hero.particle_count} particles"
        ),
        outlined=set(result.branch.local.affected_particle_ids),
        outline_color=result.protocol.render.causal_cone_color,
    )
    figure.suptitle(
        "One Collision, Two Worlds — edit the past, recompute only its causal future",
        fontsize=18,
        fontweight="bold",
    )
    figure.savefig(svg_path)
    figure.savefig(pdf_path)
    plt.close(figure)


def _render_video(result: MolecularTimeMachineE3Result, video_path: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to render the E3 video")
    plt = _pyplot()
    edited_by_time = {
        round(snapshot.time, 12): snapshot.state
        for snapshot in result.branch.local.simulation.snapshots
    }
    render = result.protocol.render
    with tempfile.TemporaryDirectory(prefix="time-machine-e3-frames-") as temporary:
        directory = Path(temporary)
        frame_index = 0
        for baseline_snapshot in result.timeline.result.snapshots:
            time = baseline_snapshot.time
            if time <= result.fork_checkpoint.time:
                edited_state = baseline_snapshot.state
                affected_ids = set(result.target_event.pair)
                outline_color = render.edited_highlight_color
            else:
                edited_state = edited_by_time[round(time, 12)]
                affected_ids = set(_affected_at_time(result, time))
                outline_color = render.causal_cone_color
            figure, axes = plt.subplots(1, 2, figsize=(12.8, 6.4), constrained_layout=True)
            _scatter_state(
                axes[0],
                baseline_snapshot.state,
                result,
                title="Original collision history",
                outlined=(affected_ids if time <= result.fork_checkpoint.time else set()),
                outline_color=outline_color,
            )
            _scatter_state(
                axes[1],
                edited_state,
                result,
                title=(
                    "Edited history"
                    if time > result.fork_checkpoint.time
                    else "Same world — edit has not happened"
                ),
                outlined=affected_ids,
                outline_color=outline_color,
            )
            phase = (
                "select collision #2"
                if time <= result.fork_checkpoint.time
                else "+1° relative-velocity edit; causal cone grows only on contact"
            )
            figure.suptitle(
                f"One Collision, Two Worlds   t={time:.2f}\n{phase}",
                fontsize=17,
                fontweight="bold",
            )
            frame = directory / f"frame-{frame_index:06d}.png"
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
    result: MolecularTimeMachineE3Result,
    *,
    title: str,
    outlined: set[int] | None = None,
    outline_color: str = "#ffb000",
) -> None:
    render = result.protocol.render
    outlined = outlined or set()
    facecolors = [
        render.foreground_color
        if result.colors.label(particle_id) == 1
        else render.background_color
        for particle_id in state.particle_ids
    ]
    edgecolors = [
        outline_color if particle_id in outlined else "#11151c"
        for particle_id in state.particle_ids
    ]
    linewidths = [2.0 if particle_id in outlined else 0.35 for particle_id in state.particle_ids]
    axis.scatter(
        [position[0] for position in state.positions],
        [position[1] for position in state.positions],
        s=38,
        c=facecolors,
        edgecolors=edgecolors,
        linewidths=linewidths,
    )
    domain = result.protocol.e1_protocol.domain
    axis.set_xlim(domain.lower[0], domain.upper[0])
    axis.set_ylim(domain.lower[1], domain.upper[1])
    axis.set_aspect("equal")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.set_title(title, fontsize=11, fontweight="bold")


def _affected_at_time(
    result: MolecularTimeMachineE3Result,
    time: float,
) -> tuple[int, ...]:
    affected: tuple[int, ...] = ()
    for event_time, particles in result.branch.local.affected_history:
        if event_time <= time + 1.0e-12:
            affected = particles
        else:
            break
    return affected


def _pyplot() -> Any:
    try:
        matplotlib = importlib.import_module("matplotlib")
        matplotlib.use("Agg")
        return importlib.import_module("matplotlib.pyplot")
    except ImportError as exc:
        raise RuntimeError("E3 rendering requires the analysis extra") from exc
