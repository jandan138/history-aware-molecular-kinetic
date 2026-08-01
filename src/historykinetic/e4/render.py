# ruff: noqa: E501
"""Neutral visual and browser artifacts for the E4 causal-steering session."""

from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from historykinetic.echo.artifacts import refresh_manifest
from historykinetic.solvers import DiskState

from .models import MolecularTimeMachineE4Result


def render_molecular_time_machine_e4(
    result: MolecularTimeMachineE4Result,
    output_directory: Path,
) -> tuple[Path, Path, Path, Path]:
    """Render the paper figure, neutral video, and self-contained local viewer."""

    output_directory.mkdir(parents=True, exist_ok=True)
    svg_path = output_directory / "figure-causal-steering.svg"
    pdf_path = output_directory / "figure-causal-steering.pdf"
    video_path = output_directory / "causal-steering-erase-one-stroke.mp4"
    viewer_path = output_directory / "causal-steering.html"
    _render_figure(result, svg_path, pdf_path)
    _render_video(result, video_path)
    _render_viewer(result, viewer_path)
    render = result.protocol.render
    frame_count = len(result.timeline.result.snapshots) * render.frame_repeat
    duration = (frame_count + render.final_hold_frames) / render.fps
    manifest_path = output_directory / "render-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "render_id": "CAUSAL-STEERING-ERASE-ONE-STROKE-v0",
                "study_id": result.protocol.study_id,
                "hero": {
                    "target_id": result.target.target_id,
                    "target_particle_ids": list(result.target.particle_ids),
                    "selected_event_id": result.selected_preview.candidate.event.event_id,
                    "selected_pair": list(result.selected_preview.candidate.event.pair),
                    "selected_angle_degrees": result.selected_preview.angle_degrees,
                },
                "comparison_lock": {
                    "camera": "fixed-orthographic-domain",
                    "timeline": "identical-physical-time",
                    "particle_display": "identical-across-worlds",
                    "passive_colors": "inherited-from-E1",
                },
                "physics_edit_applied_by_simulator": True,
                "preview_mode": "cached-exact-local-causal-branches",
                "final_branch_verified_by_full_resimulation": True,
                "renderer_mutates_physics_state": False,
                "temporal_interpolation": False,
                "posthoc_particle_correction": False,
                "video_duration_seconds": duration,
                "outputs": [
                    svg_path.name,
                    pdf_path.name,
                    video_path.name,
                    viewer_path.name,
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    refresh_manifest(output_directory)
    return svg_path, pdf_path, video_path, viewer_path


def _render_figure(
    result: MolecularTimeMachineE4Result,
    svg_path: Path,
    pdf_path: Path,
) -> None:
    plt = _pyplot()
    figure = plt.figure(figsize=(16.0, 8.7), constrained_layout=True)
    grid = figure.add_gridspec(2, 3, height_ratios=(0.9, 1.1))
    target_ids = set(result.target.particle_ids)

    target_axis = figure.add_subplot(grid[0, 0])
    _scatter_state(
        target_axis,
        result.timeline.result.snapshots[-1].state,
        result,
        title="1  Select the future feature",
        outlined=target_ids,
        outline_color=result.protocol.render.target_color,
    )
    _draw_target_bounds(target_axis, result)
    target_axis.text(
        2.08,
        1.67,
        "upper stroke\n4 foreground particles",
        color=result.protocol.render.target_color,
        fontsize=9,
        fontweight="bold",
    )

    timeline_axis = figure.add_subplot(grid[0, 1:])
    _draw_ranking_timeline(timeline_axis, result)

    baseline_axis = figure.add_subplot(grid[1, 0])
    _scatter_state(
        baseline_axis,
        result.timeline.result.snapshots[-1].state,
        result,
        title="Original future",
        outlined=target_ids,
        outline_color=result.protocol.render.target_color,
    )
    _draw_target_bounds(baseline_axis, result)

    edited_axis = figure.add_subplot(grid[1, 1])
    _scatter_state(
        edited_axis,
        result.selected_branch.local.simulation.snapshots[-1].state,
        result,
        title=(
            "Directed future  "
            f"collision #{result.selected_preview.candidate.event.ordinal}, "
            f"{result.selected_preview.angle_degrees:+g}°"
        ),
        outlined=target_ids,
        outline_color=result.protocol.render.selected_color,
    )
    _draw_target_bounds(edited_axis, result)

    outcome_axis = figure.add_subplot(grid[1, 2])
    _draw_outcome_card(outcome_axis, result)

    figure.suptitle(
        "Causal Steering — select a future feature, locate one past collision, direct a new world",
        fontsize=17,
        fontweight="bold",
    )
    figure.savefig(svg_path)
    figure.savefig(pdf_path)
    plt.close(figure)


def _draw_ranking_timeline(axis: Any, result: MolecularTimeMachineE4Result) -> None:
    render = result.protocol.render
    axis.scatter(
        [event.time for event in result.timeline.events],
        [0.0] * len(result.timeline.events),
        s=15,
        color="#aab2bf",
        alpha=0.45,
    )
    for candidate in result.candidates:
        color = render.selected_color if candidate.rank == 1 else render.target_color
        marker = "*" if candidate.rank == 1 else "o"
        axis.scatter(
            [candidate.event.time],
            [0.0],
            s=150 if candidate.rank == 1 else 72,
            marker=marker,
            color=color,
            zorder=5,
        )
        axis.annotate(
            (
                f"#{candidate.rank}: collision {candidate.event.ordinal}\n"
                f"coverage {candidate.coverage:.0%}, purity {candidate.purity:.0%}"
            ),
            xy=(candidate.event.time, 0.0),
            xytext=(candidate.event.time + 0.045, 0.08 + 0.04 * (candidate.rank - 1)),
            arrowprops={"arrowstyle": "->", "color": color, "linewidth": 1.0},
            color=color,
            fontsize=8.5,
            fontweight="bold" if candidate.rank == 1 else "normal",
        )
    axis.axvline(
        result.selected_preview.candidate.event.time,
        color=render.selected_color,
        linewidth=1.2,
    )
    axis.set_xlim(0.0, result.protocol.end_time)
    axis.set_ylim(-0.15, 0.26)
    axis.set_yticks([])
    axis.set_xlabel("reverse-future time")
    axis.set_title("2  Trace the selected feature back to causal collisions", fontweight="bold")


def _draw_outcome_card(axis: Any, result: MolecularTimeMachineE4Result) -> None:
    metrics = result.metrics
    comparison = result.selected_branch.comparison
    axis.axis("off")
    axis.set_title("3  Save one directed branch", fontweight="bold")
    card = (
        f"Selected target changes\n"
        f"  {metrics.target_ejection_fraction:.0%}  "
        f"({len(result.target.particle_ids)} particles)\n\n"
        f"Other E foreground leaves E\n"
        f"  {metrics.collateral_ejection_fraction:.0%}\n\n"
        f"Target / collateral\n"
        f"  {metrics.target_to_collateral_ratio:.1f}x\n\n"
        f"Exact preview median\n"
        f"  {metrics.preview_median_seconds * 1000:.0f} ms\n\n"
        f"Reused baseline collisions\n"
        f"  {metrics.selected_branch_reuse_fraction:.0%}\n\n"
        f"Final local/full agreement\n"
        f"  {comparison.collision_pair_agreement:.0%}"
    )
    axis.text(
        0.06,
        0.93,
        card,
        va="top",
        fontsize=12,
        family="monospace",
        bbox={"boxstyle": "round,pad=0.8", "facecolor": "#f5f7fa", "edgecolor": "#c7ced8"},
    )


def _render_video(result: MolecularTimeMachineE4Result, video_path: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to render the E4 video")
    plt = _pyplot()
    edited_by_time = {
        round(snapshot.time, 12): snapshot.state
        for snapshot in result.selected_branch.local.simulation.snapshots
    }
    render = result.protocol.render
    with tempfile.TemporaryDirectory(prefix="causal-steering-e4-frames-") as temporary:
        directory = Path(temporary)
        frame_index = 0
        for baseline_snapshot in result.timeline.result.snapshots:
            time = baseline_snapshot.time
            if time <= result.selected_checkpoint.time:
                edited_state = baseline_snapshot.state
                outlined = set(result.selected_preview.candidate.event.pair)
                outline_color = render.selected_color
                phase = "future target selected → recommended collision is in the past"
            else:
                edited_state = edited_by_time[round(time, 12)]
                outlined = _affected_at_time(result, time)
                outline_color = render.causal_cone_color
                phase = (
                    f"collision #{result.selected_preview.candidate.event.ordinal}, "
                    f"{result.selected_preview.angle_degrees:+g}° → directed future"
                )
            figure, axes = plt.subplots(1, 2, figsize=(12.8, 6.4), constrained_layout=True)
            _scatter_state(
                axes[0],
                baseline_snapshot.state,
                result,
                title="Original history",
                outlined=set(result.target.particle_ids),
                outline_color=render.target_color,
            )
            _scatter_state(
                axes[1],
                edited_state,
                result,
                title="Causal-steering branch",
                outlined=outlined,
                outline_color=outline_color,
            )
            _draw_target_bounds(axes[0], result)
            _draw_target_bounds(axes[1], result)
            figure.suptitle(
                f"Choose the Cause, Direct the Future   t={time:.2f}\n{phase}",
                fontsize=16,
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


def _render_viewer(result: MolecularTimeMachineE4Result, viewer_path: Path) -> None:
    data = _viewer_data(result)
    viewer_path.write_text(
        _viewer_html().replace("__CAUSAL_STEERING_DATA__", json.dumps(data)),
        encoding="utf-8",
    )


def _viewer_data(result: MolecularTimeMachineE4Result) -> dict[str, Any]:
    terminal = result.timeline.result.snapshots[-1].state
    return {
        "title": "Causal Steering — Erase One Stroke",
        "domain": {
            "lower": result.protocol.e1_protocol.domain.lower,
            "upper": result.protocol.e1_protocol.domain.upper,
        },
        "colors": {
            "foreground": result.protocol.render.foreground_color,
            "background": result.protocol.render.background_color,
            "target": result.protocol.render.target_color,
            "selected": result.protocol.render.selected_color,
        },
        "particle_ids": terminal.particle_ids,
        "labels": result.colors.labels_by_particle_id,
        "target": {
            "description": result.target.description,
            "particle_ids": result.target.particle_ids,
            "x_bounds": result.target.x_bounds,
            "y_bounds": result.target.y_bounds,
        },
        "baseline": {"positions": terminal.positions},
        "candidates": [
            {
                "rank": candidate.rank,
                "event_id": candidate.event.event_id,
                "ordinal": candidate.event.ordinal,
                "pair": candidate.event.pair,
                "time": candidate.event.time,
                "coverage": candidate.coverage,
                "purity": candidate.purity,
            }
            for candidate in result.candidates
        ],
        "previews": [
            {
                "event_id": preview.candidate.event.event_id,
                "angle": preview.angle_degrees,
                "positions": preview.preview.local.simulation.snapshots[-1].state.positions,
                "target_ejection": preview.target_metrics.target_ejection_fraction,
                "collateral_ejection": preview.target_metrics.collateral_ejection_fraction,
                "ratio": preview.target_metrics.target_to_collateral_ratio,
                "local_ms": preview.preview.local_seconds * 1000.0,
            }
            for preview in result.palette
        ],
        "selected": {
            "event_id": result.selected_preview.candidate.event.event_id,
            "angle": result.selected_preview.angle_degrees,
        },
        "verification": {
            "pair_agreement": result.selected_branch.comparison.collision_pair_agreement,
            "reuse": result.metrics.selected_branch_reuse_fraction,
        },
    }


def _viewer_html() -> str:
    return """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Causal Steering — Erase One Stroke</title>
<style>
  :root { color-scheme: light; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
  body { margin: 0; background: #edf1f5; color: #18212f; }
  main { max-width: 1180px; margin: 0 auto; padding: 28px; }
  h1 { margin: 0 0 6px; font-size: 28px; } p { line-height: 1.5; }
  .sub { color: #576274; max-width: 850px; }
  .card { background: white; border: 1px solid #d6dde6; border-radius: 12px; padding: 18px; margin-top: 18px; box-shadow: 0 2px 12px #2530440d; }
  .steps { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
  .step { border-left: 3px solid #ffb000; padding: 8px 12px; background: #fffaf0; }
  .step strong { display: block; margin-bottom: 3px; }
  .controls { display: grid; grid-template-columns: 1.2fr 1fr; gap: 18px; align-items: start; }
  .button-list { display: flex; flex-wrap: wrap; gap: 8px; }
  button { appearance: none; border: 1px solid #b8c2cf; border-radius: 7px; background: #f8fafc; padding: 8px 10px; cursor: pointer; font: inherit; }
  button:hover { border-color: #68778d; } button.active { color: white; background: #ff4f87; border-color: #ff4f87; }
  canvas { width: 100%; max-width: 1120px; aspect-ratio: 2 / 0.8; display: block; background: #fff; border: 1px solid #d6dde6; border-radius: 10px; }
  #readout { margin: 0; white-space: pre-line; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; line-height: 1.65; }
  .note { color: #576274; font-size: 13px; margin-bottom: 0; }
  @media (max-width: 720px) { .steps, .controls { grid-template-columns: 1fr; } main { padding: 18px; } }
</style>
<main>
  <h1>Causal Steering — Erase One Stroke</h1>
  <p class="sub">A compact local interaction artifact for the registered E4 Hero. Choose the future feature, inspect the baseline ancestry recommendation, then browse exact cached causal-branch previews. The saved choice alone was verified against a complete resimulation.</p>
  <section class="card steps">
    <div class="step"><strong>1. Select a consequence</strong><span id="target-text"></span></div>
    <div class="step"><strong>2. Find a cause</strong>Collision ranking uses only the unedited causal timeline.</div>
    <div class="step"><strong>3. Direct a future</strong>Choose a small physical rotation and inspect its exact preview.</div>
  </section>
  <section class="card controls">
    <div><strong>Recommended past collisions</strong><p class="note">Ranked by target coverage and purity in the baseline collision DAG.</p><div id="candidate-buttons" class="button-list"></div></div>
    <div><strong>Relative-velocity angle</strong><p class="note">Each option is one cached exact local causal branch.</p><div id="angle-buttons" class="button-list"></div></div>
  </section>
  <section class="card"><canvas id="worlds" width="1120" height="448"></canvas></section>
  <section class="card"><strong>Branch readout</strong><p id="readout"></p><p class="note">The browser changes no physics. It displays the registered exact preview palette. Saving the highlighted E4 choice triggers the single full-resimulation oracle recorded in the evidence package.</p></section>
</main>
<script>
const DATA = __CAUSAL_STEERING_DATA__;
const targetSet = new Set(DATA.target.particle_ids);
let selectedEvent = DATA.selected.event_id;
let selectedAngle = DATA.selected.angle;
const $ = (id) => document.getElementById(id);
$('target-text').textContent = DATA.target.description + '.';
function candidateById(id) { return DATA.candidates.find((candidate) => candidate.event_id === id); }
function previewsFor(id) { return DATA.previews.filter((preview) => preview.event_id === id); }
function currentPreview() { return previewsFor(selectedEvent).find((preview) => preview.angle === selectedAngle); }
function makeButtons() {
  const candidates = $('candidate-buttons'); candidates.replaceChildren();
  DATA.candidates.forEach((candidate) => {
    const button = document.createElement('button');
    button.textContent = `#${candidate.rank}  collision ${candidate.ordinal}  (${candidate.coverage*100|0}% target)`;
    button.className = candidate.event_id === selectedEvent ? 'active' : '';
    button.onclick = () => { selectedEvent = candidate.event_id; selectedAngle = previewsFor(selectedEvent)[0].angle; makeButtons(); draw(); };
    candidates.append(button);
  });
  const angles = $('angle-buttons'); angles.replaceChildren();
  previewsFor(selectedEvent).forEach((preview) => {
    const button = document.createElement('button');
    button.textContent = `${preview.angle > 0 ? '+' : ''}${preview.angle}°`;
    button.className = preview.angle === selectedAngle ? 'active' : '';
    button.onclick = () => { selectedAngle = preview.angle; makeButtons(); draw(); };
    angles.append(button);
  });
}
function drawWorld(ctx, positions, x0, title, edited) {
  const width = 510, height = 320, y0 = 82;
  ctx.fillStyle = '#2c3340'; ctx.fillRect(x0, y0, width, height);
  ctx.strokeStyle = DATA.colors.target; ctx.lineWidth = 2;
  const [xl, xr] = DATA.target.x_bounds, [yl, yr] = DATA.target.y_bounds;
  const [dx0, dy0] = DATA.domain.lower, [dx1, dy1] = DATA.domain.upper;
  const px = (x) => x0 + (x-dx0)/(dx1-dx0)*width;
  const py = (y) => y0 + height - (y-dy0)/(dy1-dy0)*height;
  ctx.strokeRect(px(xl), py(yr), px(xr)-px(xl), py(yl)-py(yr));
  positions.forEach((position, index) => {
    const id = DATA.particle_ids[index];
    ctx.beginPath(); ctx.arc(px(position[0]), py(position[1]), 4.1, 0, Math.PI*2);
    ctx.fillStyle = DATA.labels[id] ? DATA.colors.foreground : DATA.colors.background;
    ctx.fill();
    if (targetSet.has(id)) { ctx.strokeStyle = edited ? DATA.colors.selected : DATA.colors.target; ctx.lineWidth = 2; ctx.stroke(); }
    else { ctx.strokeStyle = '#11151c'; ctx.lineWidth = .7; ctx.stroke(); }
  });
  ctx.fillStyle = '#18212f'; ctx.font = '600 16px system-ui'; ctx.fillText(title, x0, 42);
}
function draw() {
  const preview = currentPreview(), candidate = candidateById(selectedEvent), canvas = $('worlds'), ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
  drawWorld(ctx, DATA.baseline.positions, 38, 'Original future — selected target', false);
  drawWorld(ctx, preview.positions, 574, `Exact preview — collision ${candidate.ordinal}, ${preview.angle > 0 ? '+' : ''}${preview.angle}°`, true);
  const full = candidate.event_id === DATA.selected.event_id && preview.angle === DATA.selected.angle;
  $('readout').textContent = `collision #${candidate.ordinal}, pair (${candidate.pair.join(', ')}), at t=${candidate.time.toFixed(3)}\n` +
    `baseline causal score: coverage ${(candidate.coverage*100).toFixed(0)}%, purity ${(candidate.purity*100).toFixed(0)}%\n` +
    `target leaves selected stroke: ${(preview.target_ejection*100).toFixed(0)}%\n` +
    `other foreground leaves E: ${(preview.collateral_ejection*100).toFixed(0)}%\n` +
    `target / collateral: ${preview.ratio.toFixed(1)}x\n` +
    `exact local preview: ${preview.local_ms.toFixed(0)} ms\n` +
    (full ? `saved E4 branch • full reference pair agreement ${(DATA.verification.pair_agreement*100).toFixed(0)}% • baseline reuse ${(DATA.verification.reuse*100).toFixed(0)}%` : 'preview branch • choose the highlighted saved E4 branch for the single full reference check');
}
makeButtons(); draw();
</script>
</html>
"""


def _scatter_state(
    axis: Any,
    state: DiskState,
    result: MolecularTimeMachineE4Result,
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


def _draw_target_bounds(axis: Any, result: MolecularTimeMachineE4Result) -> None:
    plt = _pyplot()
    x0, x1 = result.target.x_bounds
    y0, y1 = result.target.y_bounds
    axis.add_patch(
        plt.Rectangle(
            (x0, y0),
            x1 - x0,
            y1 - y0,
            fill=False,
            linewidth=1.25,
            linestyle="--",
            edgecolor=result.protocol.render.target_color,
        )
    )


def _affected_at_time(result: MolecularTimeMachineE4Result, time: float) -> set[int]:
    affected: set[int] = set()
    for event_time, particle_ids in result.selected_branch.local.affected_history:
        if event_time <= time + 1.0e-12:
            affected = set(particle_ids)
        else:
            break
    return affected


def _pyplot() -> Any:
    try:
        matplotlib = importlib.import_module("matplotlib")
        matplotlib.use("Agg")
        return importlib.import_module("matplotlib.pyplot")
    except ImportError as exc:
        raise RuntimeError("E4 rendering requires the analysis extra") from exc
