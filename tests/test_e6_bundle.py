from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

import jsonschema
import pytest

from historykinetic.e6 import BranchFrames, E6Shot, write_shot_bundle

ROOT = Path(__file__).resolve().parents[1]


def _shot(source: Path) -> E6Shot:
    original = BranchFrames(
        branch_id="original-e",
        label="Original",
        positions=(((0.1, 0.2), (0.3, 0.4)), ((0.2, 0.2), (0.4, 0.4))),
        velocities=(((1.0, 0.0), (0.0, 1.0)), ((1.0, 0.0), (0.0, 1.0))),
    )
    chosen = BranchFrames(
        branch_id="chosen-c",
        label="Chosen",
        positions=(((0.1, 0.2), (0.3, 0.4)), ((0.2, 0.3), (0.4, 0.5))),
        velocities=(((0.0, 1.0), (1.0, 0.0)), ((0.0, 1.0), (1.0, 0.0))),
    )
    return E6Shot(
        shot_id="same-present-hero",
        study_id="TEST-E6",
        story_act="E5",
        times=(0.8, 1.0),
        particle_ids=(10, 11),
        passive_colors=(1, 0),
        radius=0.01,
        domain_lower=(0.0, 0.0),
        domain_upper=(4.0, 2.0),
        branches=(original, chosen),
        roles={"foreground": (10,), "edited": (10, 11)},
        events={"kind": "velocity-ownership-surgery"},
        metrics={"touched_particle_count": 2},
        source_paths=(source,),
        pivot_time=0.8,
    )


def test_shot_bundle_is_deterministic_and_planar(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text('{"frozen":true}\n', encoding="utf-8")
    output = tmp_path / "bundle"
    first = write_shot_bundle(_shot(source), output, repo_root=tmp_path)
    first_bytes = first.read_bytes()
    first_position_hash = hashlib.sha256((output / "positions.f32").read_bytes()).hexdigest()
    second = write_shot_bundle(_shot(source), output, repo_root=tmp_path)

    assert second.read_bytes() == first_bytes
    assert (
        hashlib.sha256((output / "positions.f32").read_bytes()).hexdigest()
        == first_position_hash
    )
    values = struct.unpack("<" + "f" * 24, (output / "positions.f32").read_bytes())
    assert values[2] == 0.0
    assert values[5] == 0.0


def test_shot_manifest_validates_against_schema(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text("{}\n", encoding="utf-8")
    manifest_path = write_shot_bundle(_shot(source), tmp_path / "bundle", repo_root=tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / "schemas" / "e6-shot-bundle.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.Draft202012Validator(schema).validate(manifest)
    assert manifest["physics"]["renderer_modifies_physics"] is False
    assert manifest["arrays"]["shape"] == [2, 2, 2, 3]


def test_shot_rejects_role_ids_outside_particle_set(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text("{}\n", encoding="utf-8")
    shot = _shot(source)
    with pytest.raises(ValueError, match="unknown particle IDs"):
        E6Shot(
            shot_id=shot.shot_id,
            study_id=shot.study_id,
            story_act=shot.story_act,
            times=shot.times,
            particle_ids=shot.particle_ids,
            passive_colors=shot.passive_colors,
            radius=shot.radius,
            domain_lower=shot.domain_lower,
            domain_upper=shot.domain_upper,
            branches=shot.branches,
            roles={"edited": (999,)},
            events=shot.events,
            metrics=shot.metrics,
            source_paths=shot.source_paths,
            pivot_time=shot.pivot_time,
        )
