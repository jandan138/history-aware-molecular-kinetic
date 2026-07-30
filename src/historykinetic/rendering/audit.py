"""Fairness audits for primary render-manifest comparisons."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence


def audit_manifests(
    manifests: Sequence[Mapping[str, object]],
    *,
    require_complete_evidence: bool = False,
) -> list[str]:
    if len(manifests) < 2:
        return ["at least two manifests are required for a comparison audit"]

    errors: list[str] = []
    lock_digests: set[object] = set()
    display_policy_digests: set[object] = set()
    renderer_digests: set[object] = set()
    scene_ids: set[object] = set()
    schedules: set[str] = set()
    outputs: set[str] = set()
    cameras: set[str] = set()

    for index, manifest in enumerate(manifests):
        config = manifest.get("config")
        renderer = manifest.get("renderer")
        evidence = manifest.get("evidence_links")
        if not isinstance(config, Mapping):
            errors.append(f"manifest[{index}] has no config object")
            continue
        if not isinstance(renderer, Mapping):
            errors.append(f"manifest[{index}] has no renderer object")
            continue
        if manifest.get("physics_state_mutated") is not False:
            errors.append(f"manifest[{index}] reports mutated physics state")

        lock_digests.add(config.get("comparison_lock_digest"))
        display_policy_digests.add(config.get("display_policy_digest"))
        renderer_digests.add(renderer.get("digest"))
        scene_ids.add(config.get("scene_id"))
        schedules.add(_canonical(manifest.get("timeline")))
        outputs.add(_canonical(manifest.get("output")))
        cameras.add(_canonical(manifest.get("camera")))

        if require_complete_evidence:
            if not isinstance(evidence, Mapping) or evidence.get("complete") is not True:
                errors.append(f"manifest[{index}] has incomplete evidence links")

    if None in lock_digests:
        errors.append("primary comparison manifest has no comparison-lock digest")
    if len(lock_digests) != 1:
        errors.append(f"comparison-lock digests differ: {sorted(map(str, lock_digests))}")
    if None in display_policy_digests:
        errors.append("primary comparison manifest has no display-policy digest")
    if len(display_policy_digests) != 1:
        errors.append(
            "display-policy digests differ: "
            f"{sorted(map(str, display_policy_digests))}"
        )
    if len(renderer_digests) != 1:
        errors.append(f"renderer digests differ: {sorted(map(str, renderer_digests))}")
    if len(scene_ids) != 1:
        errors.append(f"scene IDs differ: {sorted(map(str, scene_ids))}")
    if len(schedules) != 1:
        errors.append("frame schedules differ")
    if len(outputs) != 1:
        errors.append("output settings differ")
    if len(cameras) != 1:
        errors.append("camera paths or camera content hashes differ")
    return errors


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
