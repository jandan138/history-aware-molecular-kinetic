"""Build read-only E6 shot bundles from frozen E1/E3/E4/E5 evidence.

The bundle is deliberately renderer neutral. Blender, Genesis, and the browser
receive the same particle IDs, frame times, planar coordinates, roles, events, and
metrics. None of the consumers can send changes back to the simulator.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib
import json
import struct
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

E6_SHOT_IDS = ("reveal-echo", "branch-collision", "choose-cause", "same-present-hero")
_TIME_DIGITS = 12


Frame2D = tuple[tuple[float, float], ...]


@dataclass(frozen=True, slots=True)
class BranchFrames:
    """One named physical branch sampled on the shot's common timeline."""

    branch_id: str
    label: str
    positions: tuple[Frame2D, ...]
    velocities: tuple[Frame2D, ...]

    def __post_init__(self) -> None:
        if not self.branch_id:
            raise ValueError("branch_id must not be empty")
        if len(self.positions) != len(self.velocities):
            raise ValueError("position and velocity frame counts must match")
        if not self.positions:
            raise ValueError("a branch requires at least one frame")
        particle_count = len(self.positions[0])
        if particle_count == 0:
            raise ValueError("a branch requires at least one particle")
        for positions, velocities in zip(self.positions, self.velocities, strict=True):
            if len(positions) != particle_count or len(velocities) != particle_count:
                raise ValueError("all branch frames must have the same particle count")


@dataclass(frozen=True, slots=True)
class E6Shot:
    """In-memory description of a versioned renderer-neutral shot."""

    shot_id: str
    study_id: str
    story_act: str
    times: tuple[float, ...]
    particle_ids: tuple[int, ...]
    passive_colors: tuple[int, ...]
    radius: float
    domain_lower: tuple[float, float]
    domain_upper: tuple[float, float]
    branches: tuple[BranchFrames, ...]
    roles: Mapping[str, tuple[int, ...]]
    events: Mapping[str, object]
    metrics: Mapping[str, object]
    source_paths: tuple[Path, ...]
    pivot_time: float | None = None

    def __post_init__(self) -> None:
        if self.shot_id not in E6_SHOT_IDS:
            raise ValueError(f"unknown E6 shot_id: {self.shot_id}")
        if not self.times or any(
            b <= a for a, b in zip(self.times, self.times[1:], strict=False)
        ):
            raise ValueError("shot times must be strictly increasing")
        if len(self.particle_ids) != len(self.passive_colors):
            raise ValueError("particle IDs and passive colors must have equal length")
        if len(set(self.particle_ids)) != len(self.particle_ids):
            raise ValueError("particle IDs must be unique")
        if self.radius <= 0:
            raise ValueError("particle radius must be positive")
        for branch in self.branches:
            if len(branch.positions) != len(self.times):
                raise ValueError("all branches must use the common shot timeline")
            if len(branch.positions[0]) != len(self.particle_ids):
                raise ValueError("branch particle count must match particle IDs")
        known_ids = set(self.particle_ids)
        for name, role_ids in self.roles.items():
            if not name or not set(role_ids).issubset(known_ids):
                raise ValueError(f"role {name!r} contains unknown particle IDs")


def build_shot(repo_root: Path, shot_id: str) -> E6Shot:
    """Load one frozen shot from ``repo_root/results``."""

    if shot_id == "reveal-echo":
        return _build_e1(repo_root)
    if shot_id == "branch-collision":
        return _build_e3(repo_root)
    if shot_id == "choose-cause":
        return _build_e4(repo_root)
    if shot_id == "same-present-hero":
        return _build_e5(repo_root)
    raise ValueError(f"unknown E6 shot_id: {shot_id}")


def export_shot(repo_root: Path, output_root: Path, shot_id: str) -> Path:
    """Build and write one frozen E6 shot bundle."""

    shot = build_shot(repo_root, shot_id)
    return write_shot_bundle(shot, output_root / shot_id, repo_root=repo_root)


def export_shots(
    repo_root: Path,
    output_root: Path,
    shot_ids: Iterable[str] = E6_SHOT_IDS,
) -> tuple[Path, ...]:
    """Export several shots and return their manifest paths."""

    return tuple(export_shot(repo_root, output_root, shot_id) for shot_id in shot_ids)


def write_shot_bundle(shot: E6Shot, output_directory: Path, *, repo_root: Path) -> Path:
    """Write a deterministic binary/JSON E6 shot bundle."""

    output_directory.mkdir(parents=True, exist_ok=True)
    position_path = output_directory / "positions.f32"
    velocity_path = output_directory / "velocities.f32"
    times_path = output_directory / "times.f64"
    roles_path = output_directory / "roles.json"
    events_path = output_directory / "events.json"
    metrics_path = output_directory / "metrics.json"

    _write_vec2_as_planar_vec3(
        position_path, (branch.positions for branch in shot.branches)
    )
    _write_vec2_as_planar_vec3(
        velocity_path, (branch.velocities for branch in shot.branches)
    )
    times_path.write_bytes(b"".join(struct.pack("<d", value) for value in shot.times))
    _write_json(roles_path, {name: list(values) for name, values in sorted(shot.roles.items())})
    _write_json(events_path, dict(shot.events))
    _write_json(metrics_path, dict(shot.metrics))

    source_artifacts = []
    for path in sorted(shot.source_paths):
        source_artifacts.append(
            {
                "path": _relative_posix(path, repo_root),
                "sha256": _sha256(path),
            }
        )
    frame_count = len(shot.times)
    particle_count = len(shot.particle_ids)
    branch_count = len(shot.branches)
    manifest: dict[str, object] = {
        "schema_version": "1.0.0",
        "shot_id": shot.shot_id,
        "study_id": shot.study_id,
        "story_act": shot.story_act,
        "physics": {
            "representation": "planar-periodic-hard-disk-edmd",
            "simulation_dimensions": 2,
            "render_dimensions": 3,
            "renderer_modifies_physics": False,
            "post_hoc_particle_correction": False,
            "coordinate_map": "physics (x,y) -> scene (x,y,radius)",
            "domain_lower": list(shot.domain_lower),
            "domain_upper": list(shot.domain_upper),
            "particle_radius": shot.radius,
        },
        "timeline": {
            "times_file": times_path.name,
            "dtype": "little-endian-float64",
            "frame_count": frame_count,
            "start_time": shot.times[0],
            "end_time": shot.times[-1],
            "pivot_time": shot.pivot_time,
        },
        "particles": {
            "count": particle_count,
            "ids": list(shot.particle_ids),
            "passive_colors": list(shot.passive_colors),
        },
        "branches": [
            {"branch_id": branch.branch_id, "label": branch.label}
            for branch in shot.branches
        ],
        "arrays": {
            "axis_order": ["branch", "frame", "particle", "xyz"],
            "shape": [branch_count, frame_count, particle_count, 3],
            "positions": {
                "path": position_path.name,
                "dtype": "little-endian-float32",
                "sha256": _sha256(position_path),
            },
            "velocities": {
                "path": velocity_path.name,
                "dtype": "little-endian-float32",
                "sha256": _sha256(velocity_path),
            },
        },
        "roles": {"path": roles_path.name, "sha256": _sha256(roles_path)},
        "events": {"path": events_path.name, "sha256": _sha256(events_path)},
        "metrics": {"path": metrics_path.name, "sha256": _sha256(metrics_path)},
        "source_artifacts": source_artifacts,
        "comparison_lock": {
            "same_camera": True,
            "same_particle_radius": True,
            "same_passive_materials": True,
            "same_frame_times": True,
            "same_lighting": True,
            "same_tone_mapping": True,
        },
    }
    manifest_without_id = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    manifest["bundle_id"] = "e6-shot-" + hashlib.sha256(
        manifest_without_id.encode("utf-8")
    ).hexdigest()[:16]
    manifest_path = output_directory / "manifest.json"
    _write_json(manifest_path, manifest)
    return manifest_path


def _build_e5(repo_root: Path) -> E6Shot:
    directory = repo_root / "results" / "molecular-time-machine-e5-v0"
    trajectory_path = directory / "same-present-trajectories.json.gz"
    payload = _read_gzip_json(trajectory_path)
    baseline = _frames(payload["baseline"])
    selected = _frames(payload["selected_after_pivot"])
    original = _branch_from_frames("original-e", "Original future — E", baseline)
    chosen = _branch_from_frames(
        "chosen-c",
        "Chosen future — C-like",
        _merge_altered_with_baseline(baseline, selected),
    )
    summary_path = directory / "summary.json"
    target_path = directory / "future-target.json"
    surgery_path = directory / "selected-surgery-manifest.json"
    palette_path = directory / "surgery-preview-palette.json"
    summary = _read_json(summary_path)
    target = _read_json(target_path)
    surgery = _read_json(surgery_path)
    palette = _read_json(palette_path)
    pivot = _float(payload["pivot_time"])
    pivot_index = _time_index(tuple(_float(frame["time"]) for frame in baseline), pivot)
    if original.positions[pivot_index] != chosen.positions[pivot_index]:
        raise ValueError("E5 branches do not share identical pivot positions")
    protocol_path = repo_root / "configs" / "studies" / "molecular-time-machine-e5-v0.json"
    protocol = _read_json(protocol_path)
    particle_ids = _int_tuple(payload["particle_ids"])
    colors = _int_tuple(payload["passive_colors"])
    authoring = _mapping(summary["authoring_session"], "authoring_session")
    selected_outcome = _mapping(summary["selected_outcome"], "selected_outcome")
    return E6Shot(
        shot_id="same-present-hero",
        study_id=str(summary["study_id"]),
        story_act="E5 — Same Present, Chosen Future",
        times=tuple(_float(frame["time"]) for frame in baseline),
        particle_ids=particle_ids,
        passive_colors=colors,
        radius=_radius(protocol, 256),
        domain_lower=(0.0, 0.0),
        domain_upper=(4.0, 2.0),
        branches=(original, chosen),
        roles={
            "foreground": tuple(
                pid for pid, color in zip(particle_ids, colors, strict=True) if color
            ),
            "target": _int_tuple(target["particle_ids"]),
            "edited": _int_tuple(authoring["touched_particle_ids"]),
            "collateral": _int_tuple(selected_outcome["collateral_retained_particle_ids"]),
        },
        events={
            "kind": "velocity-ownership-surgery",
            "pivot_time": pivot,
            "target": target,
            "selected_surgery": surgery,
            "preview_count": len(_sequence(palette["previews"], "previews")),
        },
        metrics=_mapping(summary["metrics"], "metrics"),
        source_paths=(trajectory_path, summary_path, target_path, surgery_path, palette_path),
        pivot_time=pivot,
    )


def _build_e4(repo_root: Path) -> E6Shot:
    directory = repo_root / "results" / "molecular-time-machine-e4-v0"
    trajectory_path = directory / "causal-steering-trajectories.json.gz"
    payload = _read_gzip_json(trajectory_path)
    baseline = _frames(payload["baseline"])
    altered = _frames(payload["selected"])
    summary_path = directory / "summary.json"
    target_path = directory / "causal-target.json"
    edit_path = directory / "selected-edit-manifest.json"
    ranking_path = directory / "collision-ranking.json"
    summary = _read_json(summary_path)
    target = _read_json(target_path)
    edit = _read_json(edit_path)
    ranking = _read_json(ranking_path)
    protocol = _read_json(
        repo_root / "configs" / "studies" / "molecular-time-machine-e4-v0.json"
    )
    particle_ids = _int_tuple(payload["particle_ids"])
    colors = _int_tuple(payload["passive_colors"])
    return E6Shot(
        shot_id="choose-cause",
        study_id=str(summary["study_id"]),
        story_act="E4 — Choose the Cause, Direct the Future",
        times=tuple(_float(frame["time"]) for frame in baseline),
        particle_ids=particle_ids,
        passive_colors=colors,
        radius=_radius(protocol, 128),
        domain_lower=(0.0, 0.0),
        domain_upper=(4.0, 2.0),
        branches=(
            _branch_from_frames("original-e", "Original future", baseline),
            _branch_from_frames(
                "directed-future",
                "Directed future",
                _merge_altered_with_baseline(baseline, altered),
            ),
        ),
        roles={
            "foreground": tuple(
                pid for pid, color in zip(particle_ids, colors, strict=True) if color
            ),
            "target": _int_tuple(target["particle_ids"]),
            "edited": _edit_pair(edit),
        },
        events={
            "kind": "outcome-to-cause",
            "target": target,
            "selected_edit": edit,
            "ranking": ranking,
        },
        metrics={
            "authoring_session": summary["authoring_session"],
            "causal_reuse": summary["causal_reuse"],
            "branch_correctness": summary["branch_correctness"],
        },
        source_paths=(trajectory_path, summary_path, target_path, edit_path, ranking_path),
        pivot_time=_float(edit["checkpoint_time"]),
    )


def _build_e3(repo_root: Path) -> E6Shot:
    directory = repo_root / "results" / "molecular-time-machine-e3-v0"
    trajectory_path = directory / "two-world-trajectories.json.gz"
    payload = _read_gzip_json(trajectory_path)
    baseline = _frames(payload["baseline"])
    altered = _frames(payload["edited"])
    summary_path = directory / "summary.json"
    edit_path = directory / "edit-manifest.json"
    cone_path = directory / "causal-cone.json"
    summary = _read_json(summary_path)
    edit = _read_json(edit_path)
    cone = _read_json(cone_path)
    protocol = _read_json(
        repo_root / "configs" / "studies" / "molecular-time-machine-e3-v0.json"
    )
    particle_ids = _int_tuple(payload["particle_ids"])
    colors = _int_tuple(payload["passive_colors"])
    return E6Shot(
        shot_id="branch-collision",
        study_id=str(summary["study_id"]),
        story_act="E3 — One Collision, Two Worlds",
        times=tuple(_float(frame["time"]) for frame in baseline),
        particle_ids=particle_ids,
        passive_colors=colors,
        radius=_radius(protocol, 128),
        domain_lower=(0.0, 0.0),
        domain_upper=(4.0, 2.0),
        branches=(
            _branch_from_frames("original", "Original world", baseline),
            _branch_from_frames(
                "counterfactual",
                "Counterfactual world",
                _merge_altered_with_baseline(baseline, altered),
            ),
        ),
        roles={
            "foreground": tuple(
                pid for pid, color in zip(particle_ids, colors, strict=True) if color
            ),
            "edited": _edit_pair(edit),
        },
        events={"kind": "one-collision-branch", "selected_edit": edit, "causal_cone": cone},
        metrics={
            "world_split": summary["world_split"],
            "causal_reuse": summary["causal_reuse"],
            "branch_correctness": summary["branch_correctness"],
        },
        source_paths=(trajectory_path, summary_path, edit_path, cone_path),
        pivot_time=_float(edit["checkpoint_time"]),
    )


def _build_e1(repo_root: Path) -> E6Shot:
    directory = repo_root / "results" / "molecular-echoes-e1-v0"
    trajectory_path = directory / "particle-trajectories.npz"
    summary_path = directory / "summary.json"
    protocol_path = repo_root / "configs" / "studies" / "molecular-echoes-e1-v0.json"
    np = importlib.import_module("numpy")
    with np.load(trajectory_path, allow_pickle=False) as arrays:
        positions_a = arrays["n256_seed4_exact_reverse_positions"].tolist()
        velocities_a = arrays["n256_seed4_exact_reverse_velocities"].tolist()
        positions_b = arrays["n256_seed4_chaotized_reverse_positions"].tolist()
        velocities_b = arrays["n256_seed4_chaotized_reverse_velocities"].tolist()
        colors = tuple(int(value) for value in arrays["n256_seed4_colors"].tolist())
    protocol = _read_json(protocol_path)
    timing = _mapping(protocol["timing"], "timing")
    interval = float(timing["sample_interval"])
    frame_count = len(positions_a)
    times = tuple(index * interval for index in range(frame_count))
    particle_ids = tuple(range(256))
    exact = BranchFrames(
        branch_id="exact-history",
        label="Exact collision history",
        positions=_frame2d_tuple(positions_a),
        velocities=_frame2d_tuple(velocities_a),
    )
    chaotized = BranchFrames(
        branch_id="chaotized-history",
        label="Chaotized hidden history",
        positions=_frame2d_tuple(positions_b),
        velocities=_frame2d_tuple(velocities_b),
    )
    summary = _read_json(summary_path)
    return E6Shot(
        shot_id="reveal-echo",
        study_id=str(summary["study_id"]),
        story_act="E1 — A Frame Is Not a Future",
        times=times,
        particle_ids=particle_ids,
        passive_colors=colors,
        radius=_radius(protocol, 256),
        domain_lower=(0.0, 0.0),
        domain_upper=(4.0, 2.0),
        branches=(exact, chaotized),
        roles={
            "foreground": tuple(
                pid for pid, color in zip(particle_ids, colors, strict=True) if color
            )
        },
        events={"kind": "resolved-present-opposite-futures", "seed": 4},
        metrics={
            "combined": summary["combined"],
            "n256": _mapping(summary["by_particle_count"], "by_particle_count")["256"],
        },
        source_paths=(trajectory_path, summary_path),
        pivot_time=0.0,
    )


def _branch_from_frames(
    branch_id: str,
    label: str,
    frames: tuple[dict[str, object], ...],
) -> BranchFrames:
    return BranchFrames(
        branch_id=branch_id,
        label=label,
        positions=tuple(_frame2d(frame["positions"], "positions") for frame in frames),
        velocities=tuple(_frame2d(frame["velocities"], "velocities") for frame in frames),
    )


def _merge_altered_with_baseline(
    baseline: tuple[dict[str, object], ...],
    altered: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    altered_by_time = {
        round(_float(frame["time"]), _TIME_DIGITS): frame for frame in altered
    }
    first_altered = _float(altered[0]["time"])
    merged: list[dict[str, object]] = []
    for frame in baseline:
        time = _float(frame["time"])
        if time < first_altered:
            merged.append(frame)
            continue
        key = round(time, _TIME_DIGITS)
        if key not in altered_by_time:
            raise ValueError(f"altered branch has no exact frame at t={time}")
        merged.append(altered_by_time[key])
    return tuple(merged)


def _frames(value: object) -> tuple[dict[str, object], ...]:
    frames = _sequence(value, "frames")
    return tuple(dict(_mapping(frame, "frame")) for frame in frames)


def _frame2d(value: object, label: str) -> Frame2D:
    rows = _sequence(value, label)
    output: list[tuple[float, float]] = []
    for row in rows:
        pair = _sequence(row, f"{label} row")
        if len(pair) != 2:
            raise ValueError(f"{label} rows must contain x and y")
        output.append((float(pair[0]), float(pair[1])))
    return tuple(output)


def _frame2d_tuple(value: object) -> tuple[Frame2D, ...]:
    return tuple(_frame2d(frame, "frame") for frame in _sequence(value, "frame sequence"))


def _write_vec2_as_planar_vec3(path: Path, branches: Iterable[tuple[Frame2D, ...]]) -> None:
    with path.open("wb") as handle:
        for frames in branches:
            for frame in frames:
                for x, y in frame:
                    handle.write(struct.pack("<fff", x, y, 0.0))


def _radius(protocol: Mapping[str, object], particle_count: int) -> float:
    e1_path = protocol.get("e1_protocol")
    if e1_path is not None:
        # E3-E5 inherit the E1 particle geometry.
        diameter = 0.04 if particle_count == 128 else 0.02
        return diameter / 2.0
    particle = _mapping(protocol["particle"], "particle")
    for raw in _sequence(particle["sizes"], "particle sizes"):
        size = _mapping(raw, "particle size")
        if int(size["count"]) == particle_count:
            return float(size["diameter"]) / 2.0
    raise ValueError(f"no particle size for N={particle_count}")


def _edit_pair(edit: Mapping[str, object]) -> tuple[int, ...]:
    target_pair = edit.get("target_pair")
    if target_pair is not None:
        return _int_tuple(target_pair)
    payload = _mapping(edit["edit"], "edit")
    if "particle_a" in payload and "particle_b" in payload:
        return (int(payload["particle_a"]), int(payload["particle_b"]))
    raise ValueError("edit artifact does not contain a pair")


def _time_index(times: tuple[float, ...], target: float) -> int:
    for index, time in enumerate(times):
        if abs(time - target) <= 1.0e-12:
            return index
    raise ValueError(f"timeline does not contain t={target}")


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return dict(_mapping(payload, str(path)))


def _read_gzip_json(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        payload = json.load(handle)
    return dict(_mapping(payload, str(path)))


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{label} must be a mapping")
    return value


def _sequence(value: object, label: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise TypeError(f"{label} must be a sequence")
    return value


def _int_tuple(value: object) -> tuple[int, ...]:
    return tuple(int(item) for item in _sequence(value, "integer sequence"))


def _float(value: object) -> float:
    if not isinstance(value, int | float):
        raise TypeError("expected a number")
    return float(value)


def _relative_posix(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
