# ruff: noqa: E501, RUF001
"""Paper figure, neutral video, and cached browser artifact for E5."""

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

from .models import MolecularTimeMachineE5Result


def render_molecular_time_machine_e5(
    result: MolecularTimeMachineE5Result,
    output_directory: Path,
) -> tuple[Path, Path, Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    svg_path = output_directory / "figure-same-present-chosen-future.svg"
    pdf_path = output_directory / "figure-same-present-chosen-future.pdf"
    video_path = output_directory / "same-present-two-letters.mp4"
    viewer_path = output_directory / "same-present-chosen-future.html"
    _render_figure(result, svg_path, pdf_path)
    _render_video(result, video_path)
    _render_viewer(result, viewer_path)
    render_manifest = output_directory / "render-manifest.json"
    render_manifest.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "study_id": result.protocol.study_id,
                "comparison_lock": {
                    "same_camera": True,
                    "same_particle_radius": True,
                    "same_passive_colors": True,
                    "same_time_samples": True,
                },
                "physics": {
                    "baseline": "complete EDMD",
                    "candidate_previews": "complete EDMD from the common pivot",
                    "selected": "complete EDMD from the common pivot",
                    "renderer_modifies_physics": False,
                    "post_hoc_particle_correction": False,
                },
                "interaction": {
                    "cached_exact_previews": len(result.previews),
                    "browser_runs_physics": False,
                },
                "files": [svg_path.name, pdf_path.name, video_path.name, viewer_path.name],
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
    result: MolecularTimeMachineE5Result,
    svg_path: Path,
    pdf_path: Path,
) -> None:
    plt = _pyplot()
    figure = plt.figure(figsize=(15.5, 8.4), constrained_layout=True)
    grid = figure.add_gridspec(2, 3, height_ratios=(1.0, 1.05))
    target_axis = figure.add_subplot(grid[0, 0])
    _scatter_state(
        target_axis,
        result.baseline.snapshots[-1].state,
        result,
        title="1  Creator selects the future E middle stroke",
        outlined=set(result.target.particle_ids),
        outline_color=result.protocol.render.target_color,
    )
    _draw_target_bounds(target_axis, result)

    pivot_axis = figure.add_subplot(grid[0, 1])
    _scatter_state(
        pivot_axis,
        result.pivot_state,
        result,
        title="2  The visible present stays fixed at t = 0.80",
        outlined=set(result.selected_preview.surgery.touched_particle_ids),
        outline_color=result.protocol.render.surgery_color,
    )
    _draw_swap_connections(pivot_axis, result)

    audit_axis = figure.add_subplot(grid[0, 2])
    _draw_audit_card(audit_axis, result)

    baseline_axis = figure.add_subplot(grid[1, 0])
    _scatter_state(
        baseline_axis,
        result.baseline.snapshots[-1].state,
        result,
        title="Original physical future — E",
    )
    _draw_target_bounds(baseline_axis, result)

    arrow_axis = figure.add_subplot(grid[1, 1])
    arrow_axis.axis("off")
    arrow_axis.text(
        0.5,
        0.66,
        "swap velocity ownership\ninside the same 4×2 cells",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color=result.protocol.render.surgery_color,
    )
    arrow_axis.annotate(
        "",
        xy=(0.86, 0.38),
        xytext=(0.14, 0.38),
        arrowprops={
            "arrowstyle": "-|>",
            "linewidth": 3.0,
            "color": result.protocol.render.surgery_color,
        },
    )
    arrow_axis.text(
        0.5,
        0.17,
        "4 / 256 particles touched",
        ha="center",
        fontsize=13,
        family="monospace",
    )

    edited_axis = figure.add_subplot(grid[1, 2])
    _scatter_state(
        edited_axis,
        result.selected_preview.simulation.snapshots[-1].state,
        result,
        title="Chosen physical future — C",
        outlined=set(result.target.particle_ids),
        outline_color=result.protocol.render.selected_color,
    )
    _draw_target_bounds(edited_axis, result)
    figure.suptitle(
        "Same Present, Chosen Future — keep the frame, edit hidden velocity ownership",
        fontsize=18,
        fontweight="bold",
    )
    figure.savefig(svg_path)
    figure.savefig(pdf_path)
    plt.close(figure)


def _draw_audit_card(axis: Any, result: MolecularTimeMachineE5Result) -> None:
    axis.axis("off")
    outcome = result.selected_preview.outcome
    audit = result.selected_preview.audit
    axis.set_title("3  Hidden surgery, declared present preserved", fontweight="bold")
    text = (
        "VISIBLE PRESENT\n"
        "  positions / colors     identical\n"
        "  4×2 velocity multisets identical\n\n"
        "HIDDEN EDIT\n"
        f"  swaps                   {len(result.selected_preview.surgery.swaps)}\n"
        f"  touched particles       {len(result.selected_preview.surgery.touched_particle_ids)}/256\n"
        f"  momentum error          {audit.momentum_error:.2e}\n"
        f"  energy error            {audit.energy_error:.1e}\n\n"
        "CHOSEN FUTURE\n"
        f"  middle-stroke occupancy {outcome.baseline_target_region_occupancy} → "
        f"{outcome.edited_target_region_occupancy}\n"
        f"  target removed          {outcome.target_region_reduction_fraction:.0%}\n"
        f"  rest of glyph retained  {outcome.collateral_retention_fraction:.0%}"
    )
    axis.text(
        0.04,
        0.94,
        text,
        va="top",
        fontsize=11.5,
        family="monospace",
        bbox={"boxstyle": "round,pad=0.8", "facecolor": "#f5f7fa", "edgecolor": "#c7ced8"},
    )


def _render_video(result: MolecularTimeMachineE5Result, video_path: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to render the E5 video")
    plt = _pyplot()
    selected_by_time = {
        round(result.protocol.hero.pivot_time + snapshot.time, 12): snapshot.state
        for snapshot in result.selected_preview.simulation.snapshots
    }
    pivot = result.protocol.hero.pivot_time
    render = result.protocol.render
    with tempfile.TemporaryDirectory(prefix="same-present-e5-frames-") as temporary:
        directory = Path(temporary)
        frame_index = 0
        for baseline_snapshot in result.baseline.snapshots:
            time = baseline_snapshot.time
            if time <= pivot + result.protocol.hero.recipe_tolerance:
                edited_state = baseline_snapshot.state
                phase = "one visible present — two hidden possibilities"
                highlighted = (
                    set(result.selected_preview.surgery.touched_particle_ids)
                    if abs(time - pivot) <= result.protocol.sample_interval
                    else set()
                )
            else:
                edited_state = selected_by_time[round(time, 12)]
                phase = "four particles exchange velocity ownership → futures separate"
                highlighted = set(result.target.particle_ids)
            figure, axes = plt.subplots(1, 2, figsize=(12.8, 6.4), constrained_layout=True)
            _scatter_state(
                axes[0],
                baseline_snapshot.state,
                result,
                title="Original future — E",
            )
            _scatter_state(
                axes[1],
                edited_state,
                result,
                title="Chosen future — C",
                outlined=highlighted,
                outline_color=(
                    render.surgery_color if time <= pivot else render.selected_color
                ),
            )
            if time >= pivot:
                _draw_target_bounds(axes[0], result)
                _draw_target_bounds(axes[1], result)
            figure.suptitle(
                f"Same Present, Chosen Future   t={time:.2f}\n{phase}",
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


def _render_viewer(result: MolecularTimeMachineE5Result, viewer_path: Path) -> None:
    viewer_path.write_text(
        _viewer_html().replace("__E5_DATA__", json.dumps(_viewer_data(result))),
        encoding="utf-8",
    )


def _viewer_data(result: MolecularTimeMachineE5Result) -> dict[str, Any]:
    terminal = result.baseline.snapshots[-1].state
    selected_id = result.selected_preview.surgery.surgery_id
    ordered = sorted(
        result.previews,
        key=lambda preview: (
            preview.surgery.surgery_id != selected_id,
            -preview.outcome.target_ejection_fraction,
            -preview.outcome.collateral_retention_fraction,
            preview.surgery.swaps,
        ),
    )
    return {
        "domain": {
            "lower": result.protocol.e1_protocol.domain.lower,
            "upper": result.protocol.e1_protocol.domain.upper,
        },
        "colors": {
            "foreground": result.protocol.render.foreground_color,
            "background": result.protocol.render.background_color,
            "target": result.protocol.render.target_color,
            "selected": result.protocol.render.selected_color,
            "surgery": result.protocol.render.surgery_color,
        },
        "particle_ids": terminal.particle_ids,
        "labels": result.colors.labels_by_particle_id,
        "target": {
            "description": result.target.description,
            "particle_ids": result.target.particle_ids,
            "x_bounds": result.target.x_bounds,
            "y_bounds": result.target.y_bounds,
        },
        "pivot": {"positions": result.pivot_state.positions},
        "baseline": {"positions": terminal.positions},
        "previews": [
            {
                "surgery_id": preview.surgery.surgery_id,
                "swaps": preview.surgery.swaps,
                "positions": preview.simulation.snapshots[-1].state.positions,
                "target_ejection": preview.outcome.target_ejection_fraction,
                "target_reduction": preview.outcome.target_region_reduction_fraction,
                "collateral_retention": preview.outcome.collateral_retention_fraction,
                "target_occupancy": preview.outcome.edited_target_region_occupancy,
                "selected": preview.surgery.surgery_id == selected_id,
            }
            for preview in ordered
        ],
        "selected_id": selected_id,
    }


def _viewer_html() -> str:
    return """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Same Present, Chosen Future</title>
<style>
  :root { color-scheme: light; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
  body { margin: 0; background: #edf1f5; color: #18212f; }
  main { max-width: 1240px; margin: 0 auto; padding: 28px; }
  h1 { margin: 0 0 6px; font-size: 29px; } p { line-height: 1.5; }
  .sub { color: #576274; max-width: 920px; }
  .card { background: white; border: 1px solid #d6dde6; border-radius: 12px; padding: 18px; margin-top: 18px; box-shadow: 0 2px 12px #2530440d; }
  .steps { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
  .step { border-left: 3px solid #9b8cff; padding: 8px 12px; background: #f7f5ff; }
  .step strong { display: block; margin-bottom: 3px; }
  select { font: inherit; padding: 8px 10px; border: 1px solid #b8c2cf; border-radius: 7px; max-width: 100%; }
  canvas { width: 100%; aspect-ratio: 2.45 / 0.8; display: block; background: #fff; border: 1px solid #d6dde6; border-radius: 10px; }
  #readout { margin: 12px 0 0; white-space: pre-line; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; line-height: 1.6; }
  .note { color: #576274; font-size: 13px; }
  @media (max-width: 720px) { .steps { grid-template-columns: 1fr; } main { padding: 18px; } }
</style>
<main>
  <h1>Same Present, Chosen Future</h1>
  <p class="sub">Select the future E middle stroke, keep the visible t=0.80 present fixed, and browse the registered exact velocity-ownership surgeries. The highlighted result changes E into a C-like future by touching four of 256 particles.</p>
  <section class="card steps">
    <div class="step"><strong>1. Select a future feature</strong>The horizontal extension of the E middle stroke.</div>
    <div class="step"><strong>2. Preserve the present</strong>Positions, colors, and declared 4×2 velocity multisets stay fixed.</div>
    <div class="step"><strong>3. Choose a future</strong>Each cached option is a complete EDMD evolution from the same pivot.</div>
  </section>
  <section class="card"><label for="preview"><strong>Exact surgery preview</strong></label><br><select id="preview"></select><p class="note">The browser changes no simulation state; it displays the frozen exact preview palette.</p></section>
  <section class="card"><canvas id="worlds" width="1220" height="398"></canvas><p id="readout"></p></section>
</main>
<script>
const DATA = __E5_DATA__;
const $ = (id) => document.getElementById(id);
const select = $('preview');
DATA.previews.forEach((preview, index) => {
  const option = document.createElement('option');
  option.value = String(index);
  option.textContent = `${preview.selected ? '★ selected — ' : ''}${preview.swaps.map((pair) => `(${pair.join(',')})`).join(' + ')}`;
  select.append(option);
});
function drawWorld(ctx, positions, x0, title, targetBox) {
  const width=360, height=250, y0=90, [dx0,dy0]=DATA.domain.lower, [dx1,dy1]=DATA.domain.upper;
  const px=(x)=>x0+(x-dx0)/(dx1-dx0)*width, py=(y)=>y0+height-(y-dy0)/(dy1-dy0)*height;
  ctx.fillStyle='#2c3340'; ctx.fillRect(x0,y0,width,height);
  positions.forEach((position,index)=>{ const id=DATA.particle_ids[index]; ctx.beginPath(); ctx.arc(px(position[0]),py(position[1]),3.6,0,Math.PI*2); ctx.fillStyle=DATA.labels[id]?DATA.colors.foreground:DATA.colors.background; ctx.fill(); });
  if (targetBox) { const [xl,xr]=DATA.target.x_bounds,[yl,yr]=DATA.target.y_bounds; ctx.strokeStyle=DATA.colors.target; ctx.lineWidth=2; ctx.setLineDash([6,4]); ctx.strokeRect(px(xl),py(yr),px(xr)-px(xl),py(yl)-py(yr)); ctx.setLineDash([]); }
  ctx.fillStyle='#18212f'; ctx.font='600 16px system-ui'; ctx.fillText(title,x0,48);
}
function draw(){ const preview=DATA.previews[Number(select.value||0)], canvas=$('worlds'), ctx=canvas.getContext('2d'); ctx.clearRect(0,0,canvas.width,canvas.height); ctx.fillStyle='#fff'; ctx.fillRect(0,0,canvas.width,canvas.height); drawWorld(ctx,DATA.pivot.positions,25,'Same visible present',false); drawWorld(ctx,DATA.baseline.positions,430,'Original future — E',true); drawWorld(ctx,preview.positions,835,'Chosen future — C',true); $('readout').textContent=`swaps: ${preview.swaps.map((pair)=>`(${pair.join(', ')})`).join(' + ')}\ntarget particles ejected: ${(preview.target_ejection*100).toFixed(0)}% • target region reduction: ${(preview.target_reduction*100).toFixed(0)}% • rest of glyph retained: ${(preview.collateral_retention*100).toFixed(0)}%\nterminal middle-stroke occupancy: 8 → ${preview.target_occupancy}${preview.selected?'\\nregistered E5 selection • four of 256 particles touched':''}`; }
select.addEventListener('change',draw); draw();
</script>
</html>
"""


def _scatter_state(
    axis: Any,
    state: DiskState,
    result: MolecularTimeMachineE5Result,
    *,
    title: str,
    outlined: set[int] | None = None,
    outline_color: str = "#ffb000",
) -> None:
    render = result.protocol.render
    outlined = outlined or set()
    facecolors = [
        render.foreground_color if result.colors.label(particle_id) == 1 else render.background_color
        for particle_id in state.particle_ids
    ]
    edgecolors = [
        outline_color if particle_id in outlined else "#11151c"
        for particle_id in state.particle_ids
    ]
    linewidths = [2.0 if particle_id in outlined else 0.25 for particle_id in state.particle_ids]
    axis.scatter(
        [position[0] for position in state.positions],
        [position[1] for position in state.positions],
        s=28,
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


def _draw_target_bounds(axis: Any, result: MolecularTimeMachineE5Result) -> None:
    plt = _pyplot()
    x0, x1 = result.target.x_bounds
    y0, y1 = result.target.y_bounds
    axis.add_patch(
        plt.Rectangle(
            (x0, y0),
            x1 - x0,
            y1 - y0,
            fill=False,
            linewidth=1.3,
            linestyle="--",
            edgecolor=result.protocol.render.target_color,
        )
    )


def _draw_swap_connections(axis: Any, result: MolecularTimeMachineE5Result) -> None:
    by_id = {
        particle_id: position
        for particle_id, position in zip(
            result.pivot_state.particle_ids, result.pivot_state.positions, strict=True
        )
    }
    for left, right in result.selected_preview.surgery.swaps:
        left_position = by_id[left]
        right_position = by_id[right]
        axis.plot(
            [left_position[0], right_position[0]],
            [left_position[1], right_position[1]],
            color=result.protocol.render.surgery_color,
            linewidth=2.0,
            linestyle="--",
        )


def _pyplot() -> Any:
    try:
        matplotlib = importlib.import_module("matplotlib")
        matplotlib.use("Agg")
        return importlib.import_module("matplotlib.pyplot")
    except ImportError as exc:
        raise RuntimeError("E5 rendering requires the analysis extra") from exc
