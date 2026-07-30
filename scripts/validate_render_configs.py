from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml

from historykinetic.rendering import render_summary_from_mapping

ROOT = Path(__file__).resolve().parents[1]
RENDER_ROOT = ROOT / "configs" / "render"


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def main() -> int:
    render_schema = _load_json(ROOT / "schemas" / "render-config.schema.json")
    camera_schema = _load_json(ROOT / "schemas" / "camera-path.schema.json")
    render_validator = jsonschema.Draft202012Validator(render_schema)
    camera_validator = jsonschema.Draft202012Validator(camera_schema)

    config_paths = sorted(RENDER_ROOT.rglob("*.yml"))
    if not config_paths:
        raise SystemExit("no render configurations found")

    camera_ids: dict[str, Path] = {}
    for path in sorted((RENDER_ROOT / "cameras").rglob("*.json")):
        payload = _load_json(path)
        camera_validator.validate(payload)
        camera_id = str(payload["camera_path_id"])
        if camera_id in camera_ids:
            raise ValueError(
                f"duplicate camera_path_id {camera_id}: {camera_ids[camera_id]} and {path}"
            )
        camera_ids[camera_id] = path

    for path in config_paths:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"expected YAML object: {path}")
        render_validator.validate(payload)
        summary = render_summary_from_mapping(payload)

        timeline = payload["timeline"]
        assert isinstance(timeline, dict)
        config_start = float(timeline["start_time"])
        config_end = float(timeline["end_time"])
        camera = payload["camera"]
        assert isinstance(camera, dict)
        paths = camera["paths"]
        assert isinstance(paths, list)

        for shot in paths:
            assert isinstance(shot, dict)
            shot_start = float(shot["start_time"])
            shot_end = float(shot["end_time"])
            if shot_start < config_start or shot_end > config_end or shot_end <= shot_start:
                raise ValueError(f"shot outside render timeline in {path}: {shot['shot_id']}")

            camera_path = RENDER_ROOT / str(shot["path_ref"])
            if not camera_path.exists():
                raise ValueError(f"missing camera path in {path}: {shot['path_ref']}")
            camera_digest = hashlib.sha256(camera_path.read_bytes()).hexdigest()
            if camera_digest != shot["sha256"]:
                raise ValueError(
                    f"camera digest mismatch in {path}: {shot['path_ref']} "
                    f"declares {shot['sha256']} but file is {camera_digest}"
                )
            camera_payload = _load_json(camera_path)
            camera_validator.validate(camera_payload)
            keyframes = camera_payload["keyframes"]
            assert isinstance(keyframes, list)
            first = float(keyframes[0]["time"])
            last = float(keyframes[-1]["time"])
            if first > shot_start or last < shot_end:
                raise ValueError(
                    f"camera path does not span shot {shot['shot_id']} in {path}: "
                    f"[{first}, {last}] vs [{shot_start}, {shot_end}]"
                )

        print(f"{path.relative_to(ROOT)}: {summary.stable_id}")

    print(f"validated {len(config_paths)} render configs and {len(camera_ids)} camera paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
