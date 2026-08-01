#!/usr/bin/env python3
"""Render a neutral E6 validation frame with the canonical local Genesis checkout.

This renderer is intentionally plain.  It proves that the frozen renderer-neutral
bundle can be consumed inside Genesis without re-simulating or correcting any
particle state; Blender and the browser own the cinematic presentation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
from pathlib import Path
from typing import Any

os.environ.setdefault("PYOPENGL_PLATFORM", "osmesa")

import genesis as gs
import numpy as np
from PIL import Image


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a frozen E6 bundle in Genesis")
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--frame-index", type=int, default=-1)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    return parser.parse_args()


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def _load_float32(path: Path) -> np.ndarray:
    payload = path.read_bytes()
    if len(payload) % 4:
        raise ValueError(f"invalid float32 payload: {path}")
    return np.asarray(struct.unpack(f"<{len(payload) // 4}f", payload), dtype=np.float32)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _rgba(hex_value: str, alpha: float = 1.0) -> tuple[float, float, float, float]:
    value = hex_value.lstrip("#")
    rgb = tuple(int(value[index : index + 2], 16) / 255.0 for index in (0, 2, 4))
    return (*rgb, alpha)


def _render(args: argparse.Namespace) -> None:
    bundle = args.bundle.resolve()
    manifest_path = bundle / "manifest.json"
    manifest = _load_json(manifest_path)
    roles = _load_json(bundle / str(manifest["roles"]["path"]))
    shape = tuple(int(value) for value in manifest["arrays"]["shape"])
    branch_count, frame_count, _particle_count, component_count = shape
    if component_count != 3:
        raise ValueError("E6 positions must be xyz vectors")
    frame_index = args.frame_index if args.frame_index >= 0 else frame_count - 1
    if not 0 <= frame_index < frame_count:
        raise ValueError("frame-index is outside the shot timeline")

    positions = _load_float32(bundle / str(manifest["arrays"]["positions"]["path"]))
    positions = positions.reshape(shape)
    particle_ids = np.asarray(manifest["particles"]["ids"], dtype=np.int64)
    passive_colors = np.asarray(manifest["particles"]["passive_colors"], dtype=np.int64)
    radius = float(manifest["physics"]["particle_radius"])
    target_ids = {int(value) for value in roles.get("target", [])}
    edited_ids = {int(value) for value in roles.get("edited", [])}

    gs.init(backend=gs.cpu)
    scene = gs.Scene(
        show_viewer=False,
        renderer=gs.renderers.Rasterizer(),
        vis_options=gs.options.VisOptions(
            show_world_frame=False,
            show_cameras=False,
            plane_reflection=False,
            ambient_light=(0.32, 0.35, 0.4),
            background_color=(0.012, 0.02, 0.04),
        ),
    )
    scene.add_entity(morph=gs.morphs.Plane())
    camera = scene.add_camera(
        res=(args.width, args.height),
        pos=(4.0, -0.2, 8.6),
        lookat=(4.0, 1.0, 0.0),
        fov=48,
        GUI=False,
    )

    branch_offsets = np.linspace(0.0, 4.6, branch_count, dtype=np.float32)
    for branch_index, offset in enumerate(branch_offsets):
        branch_positions = positions[branch_index, frame_index].copy()
        branch_positions[:, 0] += offset
        branch_positions[:, 2] = radius

        for particle_index, particle_id in enumerate(particle_ids):
            if int(particle_id) in edited_ids:
                color = _rgba("#ff5b6e")
            elif int(particle_id) in target_ids:
                color = _rgba("#36d6ff")
            elif passive_colors[particle_index]:
                color = _rgba("#d9e7e8")
            else:
                color = _rgba("#263040")
            scene.add_entity(
                morph=gs.morphs.Sphere(
                    pos=tuple(float(value) for value in branch_positions[particle_index]),
                    radius=radius,
                    fixed=True,
                ),
                surface=gs.surfaces.Default(color=color),
            )

    scene.build()

    rgb = camera.render(rgb=True, depth=False, segmentation=False, normal=False)[0]
    if rgb is None:
        raise RuntimeError("Genesis returned no RGB frame")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.asarray(rgb, dtype=np.uint8)).save(output)

    genesis_file = Path(gs.__file__).resolve()
    expected_genesis_file = Path("/home/zhuzihou/dev/Genesis/genesis/__init__.py")
    if genesis_file != expected_genesis_file:
        raise RuntimeError(f"unexpected Genesis import: {genesis_file}")
    evidence = {
        "schema_version": "1.0.0",
        "renderer": {
            "name": "Genesis",
            "version": gs.__version__,
            "genesis_file": genesis_file.as_posix(),
            "backend": "cpu-osmesa-rasterizer",
        },
        "shot_id": manifest["shot_id"],
        "bundle_id": manifest["bundle_id"],
        "bundle_manifest_sha256": _sha256(manifest_path),
        "frame_index": frame_index,
        "output": {"path": output.as_posix(), "sha256": _sha256(output)},
        "comparison_lock": manifest["comparison_lock"],
        "physics_state_mutated": False,
        "purpose": "neutral source-state validation; not the cinematic renderer",
    }
    manifest_output = args.manifest_output or output.with_suffix(".render-manifest.json")
    manifest_output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, sort_keys=True))
    gs.destroy()


if __name__ == "__main__":
    _render(_arguments())
