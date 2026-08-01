#!/usr/bin/env python3
"""Render one E6 shot-bundle frame in Blender.

Run with Blender, not the project interpreter::

    blender -b --python scripts/render_e6_blender.py -- \
      --bundle results/.../same-present-hero --output /tmp/e6.png --quality preview
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path
from typing import Any

import bpy  # type: ignore[import-not-found]
from mathutils import Vector  # type: ignore[import-not-found]


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a frozen E6 shot bundle")
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quality", choices=("preview", "final"), default="preview")
    parser.add_argument("--frame-index", type=int, default=-1)
    parser.add_argument("--engine", choices=("eevee", "cycles"), default=None)
    parser.add_argument("--device", choices=("optix", "cuda", "cpu"), default="optix")
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--animation", action="store_true")
    parser.add_argument("--frame-stride", type=int, default=3)
    parser.add_argument("--fps", type=int, default=24)
    values = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(values)


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"expected JSON object: {path}")
    return payload


def _load_float32(path: Path) -> tuple[float, ...]:
    data = path.read_bytes()
    if len(data) % 4:
        raise ValueError(f"invalid float32 payload: {path}")
    return struct.unpack(f"<{len(data) // 4}f", data)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _hex_rgba(value: str) -> tuple[float, float, float, float]:
    value = value.lstrip("#")
    rgb = tuple(int(value[index : index + 2], 16) / 255.0 for index in (0, 2, 4))
    return (*rgb, 1.0)


PALETTE = {
    "world": "#03050a",
    "obsidian": "#0c101a",
    "passive": "#263040",
    "foreground": "#d9e7e8",
    "target": "#36d6ff",
    "history": "#ffb000",
    "surgery": "#ff5b6e",
}


def _material(
    name: str,
    color: str,
    *,
    metallic: float = 0.0,
    roughness: float = 0.28,
    emission: float = 0.0,
) -> Any:
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    node = material.node_tree.nodes.get("Principled BSDF")
    rgba = _hex_rgba(color)
    node.inputs["Base Color"].default_value = rgba
    metallic_input = node.inputs.get("Metallic IOR") or node.inputs.get("Metallic")
    if metallic_input is None:
        raise RuntimeError("Blender Principled BSDF has no metallic input")
    metallic_input.default_value = metallic
    node.inputs["Roughness"].default_value = roughness
    if emission > 0:
        node.inputs["Emission Color"].default_value = rgba
        node.inputs["Emission Strength"].default_value = emission
    return material


def _reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras):
        for datablock in tuple(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def _look_at(obj: Any, target: tuple[float, float, float]) -> None:
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def _configure_render(
    quality: str, engine_override: str | None, device_backend: str
) -> dict[str, object]:
    scene = bpy.context.scene
    engine = engine_override or ("cycles" if quality == "final" else "eevee")
    if engine == "cycles":
        scene.render.engine = "BLENDER_EEVEE"
        try:
            preferences = bpy.context.preferences.addons["cycles"].preferences
            enabled: list[str] = []
            if device_backend == "cpu":
                for device in preferences.devices:
                    device.use = device.type == "CPU"
                    if device.use:
                        enabled.append(device.name)
            else:
                preferences.compute_device_type = device_backend.upper()
                preferences.get_devices()
                for device in preferences.devices:
                    device.use = device.type == device_backend.upper()
                    if device.use:
                        enabled.append(device.name)
                if not enabled:
                    raise RuntimeError(f"no Cycles {device_backend.upper()} device is available")
            scene.render.engine = "CYCLES"
            scene.cycles.device = "CPU" if device_backend == "cpu" else "GPU"
            scene.cycles.samples = 384 if quality == "final" else 24
            scene.cycles.use_denoising = True
        except Exception as error:  # Blender exposes backend errors only at runtime.
            raise RuntimeError(
                f"Cycles {device_backend.upper()} is required for this E6 render"
            ) from error
    else:
        enabled = []
        scene.render.engine = "BLENDER_EEVEE"
        scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_x = 3840 if quality == "final" else 960
    scene.render.resolution_y = 2160 if quality == "final" else 540
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.world.color = _hex_rgba("#000001")[:3]
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    if background is not None:
        background.inputs["Color"].default_value = _hex_rgba("#000001")
        background.inputs["Strength"].default_value = 0.025
    return {
        "engine": scene.render.engine,
        "device_backend": device_backend if engine == "cycles" else "graphics-context",
        "enabled_devices": enabled,
    }


def _create_particle_mesh(radius: float) -> Any:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=radius, location=(0, 0, 0))
    template = bpy.context.object
    mesh = template.data
    mesh.name = "E6 instanced particle sphere"
    bpy.data.objects.remove(template, do_unlink=True)
    return mesh


def _mesh_material_variant(mesh: Any, name: str, material: Any) -> Any:
    variant = mesh.copy()
    variant.name = name
    variant.materials.append(material)
    return variant


def _add_floor_and_rails(branch_offsets: list[float]) -> None:
    floor_material = _material("Obsidian", PALETTE["obsidian"], metallic=0.65, roughness=0.18)
    rail_material = _material("Chamber edge", PALETTE["target"], roughness=0.22, emission=0.45)
    for offset in branch_offsets:
        bpy.ops.mesh.primitive_cube_add(location=(offset, 0.0, -0.055), scale=(2.15, 1.15, 0.05))
        bpy.context.object.data.materials.append(floor_material)
        for x, y, sx, sy in (
            (-2.05, 0.0, 0.025, 1.05),
            (2.05, 0.0, 0.025, 1.05),
            (0.0, -1.05, 2.05, 0.025),
            (0.0, 1.05, 2.05, 0.025),
        ):
            bpy.ops.mesh.primitive_cube_add(
                location=(offset + x, y, 0.025), scale=(sx, sy, 0.025)
            )
            bpy.context.object.data.materials.append(rail_material)


def _add_text(label: str, location: tuple[float, float, float]) -> None:
    bpy.ops.object.text_add(location=location, rotation=(0.0, 0.0, 0.0))
    text = bpy.context.object
    text.data.body = label
    text.data.align_x = "CENTER"
    text.data.size = 0.22
    text.data.extrude = 0.004
    font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    if font_path.is_file():
        text.data.font = bpy.data.fonts.load(str(font_path), check_existing=True)
    text.data.materials.append(
        _material(f"Label {label}", PALETTE["foreground"], emission=0.18)
    )


def _add_lights() -> None:
    for name, location, energy, size, color in (
        ("Cyan rim", (-4.0, -2.0, 5.5), 420.0, 4.0, "#36d6ff"),
        ("Coral rim", (4.0, 1.5, 4.8), 360.0, 3.0, "#ff5b6e"),
        ("Soft key", (0.0, -1.0, 7.0), 520.0, 5.5, "#d9e7e8"),
    ):
        data = bpy.data.lights.new(name, type="AREA")
        data.energy = energy
        data.shape = "DISK"
        data.size = size
        data.color = _hex_rgba(color)[:3]
        light = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(light)
        light.location = location
        _look_at(light, (0.0, 0.0, 0.0))


def _add_camera() -> Any:
    data = bpy.data.cameras.new("E6 comparison camera")
    data.lens = 52.0
    camera = bpy.data.objects.new("E6 comparison camera", data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0.0, -7.6, 9.8)
    _look_at(camera, (0.0, 0.0, 0.0))
    bpy.context.scene.camera = camera
    return camera


def _render(args: argparse.Namespace) -> None:
    bundle = args.bundle.resolve()
    manifest_path = bundle / "manifest.json"
    manifest = _load_json(manifest_path)
    roles = _load_json(bundle / manifest["roles"]["path"])
    shape = manifest["arrays"]["shape"]
    branch_count, frame_count, particle_count, component_count = (int(value) for value in shape)
    if component_count != 3:
        raise ValueError("E6 positions must be xyz vectors")
    frame_index = args.frame_index if args.frame_index >= 0 else frame_count - 1
    if not 0 <= frame_index < frame_count:
        raise ValueError("frame-index is outside the shot timeline")
    if args.frame_stride < 1:
        raise ValueError("frame-stride must be positive")
    if args.fps < 1:
        raise ValueError("fps must be positive")
    positions = _load_float32(bundle / manifest["arrays"]["positions"]["path"])
    particle_ids = [int(value) for value in manifest["particles"]["ids"]]
    passive_colors = [int(value) for value in manifest["particles"]["passive_colors"]]
    radius = float(manifest["physics"]["particle_radius"]) * 3.5
    branches = manifest["branches"]

    _reset_scene()
    render_info = _configure_render(args.quality, args.engine, args.device)
    if args.animation:
        bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    branch_offsets = [(-2.25 if branch_count == 2 else 0.0), (2.25 if branch_count == 2 else 0.0)]
    _add_floor_and_rails(branch_offsets[:branch_count])
    _add_lights()
    _add_camera()

    passive_material = _material("Passive graphite", PALETTE["passive"], metallic=0.3)
    foreground_material = _material("Foreground pearl", PALETTE["foreground"], metallic=0.1)
    target_material = _material("Target halo", PALETTE["target"], emission=3.0)
    surgery_material = _material("Surgery halo", PALETTE["surgery"], emission=4.0)
    base_particle_mesh = _create_particle_mesh(radius)
    passive_mesh = _mesh_material_variant(
        base_particle_mesh, "Passive instanced particle", passive_material
    )
    foreground_mesh = _mesh_material_variant(
        base_particle_mesh, "Foreground instanced particle", foreground_material
    )
    base_halo_mesh = _create_particle_mesh(radius * 1.55)
    target_halo_mesh = _mesh_material_variant(base_halo_mesh, "Target halo", target_material)
    surgery_halo_mesh = _mesh_material_variant(
        base_halo_mesh, "Surgery halo", surgery_material
    )
    target_ids = set(int(value) for value in roles.get("target", []))
    edited_ids = set(int(value) for value in roles.get("edited", []))

    def particle_location(
        branch_index: int, particle_index: int, sampled_frame_index: int
    ) -> tuple[float, float, float]:
        flat_index = (
            (
                (branch_index * frame_count + sampled_frame_index) * particle_count
                + particle_index
            )
            * 3
        )
        x, y, _ = positions[flat_index : flat_index + 3]
        return (branch_offsets[branch_index] + x - 2.0, y - 1.0, radius)

    def animate_location(obj: Any, branch_index: int, particle_index: int) -> None:
        if not args.animation:
            return
        for sampled_frame_index in range(frame_count):
            obj.location = particle_location(
                branch_index, particle_index, sampled_frame_index
            )
            timeline_frame = 1 + sampled_frame_index * args.frame_stride
            obj.keyframe_insert(data_path="location", frame=timeline_frame)

    for branch_index in range(branch_count):
        offset = branch_offsets[branch_index]
        _add_text(str(branches[branch_index]["label"]), (offset, -1.38, 0.02))
        for particle_index, particle_id in enumerate(particle_ids):
            location = particle_location(branch_index, particle_index, frame_index)
            particle_mesh = foreground_mesh if passive_colors[particle_index] else passive_mesh
            particle = bpy.data.objects.new(f"b{branch_index}-p{particle_id}", particle_mesh)
            bpy.context.collection.objects.link(particle)
            particle.location = location
            animate_location(particle, branch_index, particle_index)
            halo_mesh = None
            if particle_id in edited_ids:
                halo_mesh = surgery_halo_mesh
            elif particle_id in target_ids:
                halo_mesh = target_halo_mesh
            if halo_mesh is not None:
                halo = bpy.data.objects.new(f"halo-b{branch_index}-p{particle_id}", halo_mesh)
                bpy.context.collection.objects.link(halo)
                halo.location = location
                animate_location(halo, branch_index, particle_index)
                wire = halo.modifiers.new(name="Scientific role outline", type="WIREFRAME")
                wire.thickness = radius * 0.12

    args.output.parent.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    output_path = args.output.resolve()
    scene.render.filepath = str(output_path)
    if args.animation:
        scene.frame_start = 1
        scene.frame_end = 1 + (frame_count - 1) * args.frame_stride
        scene.render.fps = args.fps
        frame_directory = output_path.parent / f"{output_path.stem}-frames"
        frame_directory.mkdir(parents=True, exist_ok=True)
        scene.render.filepath = str(frame_directory / "frame-")
        scene.render.image_settings.file_format = "PNG"
        bpy.ops.render.render(animation=True)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(args.fps),
                "-start_number",
                "1",
                "-i",
                str(frame_directory / "frame-%04d.png"),
                "-frames:v",
                str(scene.frame_end),
                "-an",
                "-c:v",
                "libx264",
                "-preset",
                "slow",
                "-crf",
                "17",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(output_path),
            ],
            check=True,
        )
    else:
        bpy.ops.render.render(write_still=True)
    evidence = {
        "schema_version": "1.0.0",
        "renderer": {
            "name": "Blender",
            "version": bpy.app.version_string,
            **render_info,
        },
        "shot_id": manifest["shot_id"],
        "bundle_id": manifest["bundle_id"],
        "bundle_manifest_sha256": _sha256(manifest_path),
        "frame_index": frame_index,
        "animation": {
            "enabled": args.animation,
            "fps": args.fps,
            "frame_start": 1 if args.animation else None,
            "frame_end": 1 + (frame_count - 1) * args.frame_stride
            if args.animation
            else None,
            "frame_stride": args.frame_stride if args.animation else None,
        },
        "output": {"path": output_path.as_posix(), "sha256": _sha256(output_path)},
        "comparison_lock": manifest["comparison_lock"],
        "physics_state_mutated": False,
    }
    manifest_output = args.manifest_output or output_path.with_suffix(".render-manifest.json")
    manifest_output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    _render(_arguments())
