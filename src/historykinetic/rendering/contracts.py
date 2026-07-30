"""Typed, renderer-agnostic contracts for reproducible visual evidence.

The visual layer records intent and provenance. It deliberately cannot contain
solver controls or mutable physics state.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath

from historykinetic.contracts import ArtifactRef
from historykinetic.ids import canonical_json, content_id


class RenderPurpose(str, Enum):
    DIAGNOSTIC = "diagnostic"
    SHARED_COMPARISON = "shared_comparison"
    HERO = "hero"


class RenderChannel(str, Enum):
    EXACT_PARTICLES = "exact_particles"
    STATISTICAL_DISPLAY_PARTICLES = "statistical_display_particles"
    GEOMETRY = "geometry"
    BLOCK_GRID = "block_grid"
    DENSITY_VOLUME = "density_volume"
    SPECIES_VOLUME = "species_volume"
    TEMPERATURE_VOLUME = "temperature_volume"
    PARTITION_MASK = "partition_mask"
    COLLISION_GRAPH = "collision_graph"
    VELOCITY_DISTRIBUTION = "velocity_distribution"
    PAIR_STATISTICS = "pair_statistics"
    CONSERVATION_TIMELINE = "conservation_timeline"
    REFERENCE_ERROR = "reference_error"
    METRICS_INSET = "metrics_inset"


PRIMARY_COMPARISON_LOCK_FIELDS = frozenset(
    {"output", "timeline", "camera", "layers", "display_policy", "postprocess"}
)


@dataclass(frozen=True, slots=True)
class FrameSchedule:
    start_time: float
    end_time: float
    sample_interval: float

    def __post_init__(self) -> None:
        if self.start_time < 0:
            raise ValueError("start_time must be non-negative")
        if self.end_time < self.start_time:
            raise ValueError("end_time must not precede start_time")
        if self.sample_interval <= 0:
            raise ValueError("sample_interval must be positive")

    @property
    def frame_count(self) -> int:
        span = self.end_time - self.start_time
        return int(round(span / self.sample_interval)) + 1


@dataclass(frozen=True, slots=True)
class ComparisonLock:
    enabled: bool
    group_id: str
    locked_fields: tuple[str, ...]
    method_specific_overrides_forbidden: bool = True

    def __post_init__(self) -> None:
        if self.enabled and not self.group_id:
            raise ValueError("enabled comparison locks require a group_id")
        if len(set(self.locked_fields)) != len(self.locked_fields):
            raise ValueError("locked_fields must be unique")
        if not self.method_specific_overrides_forbidden:
            raise ValueError("method-specific render overrides are forbidden")

    @property
    def is_primary_ready(self) -> bool:
        return self.enabled and PRIMARY_COMPARISON_LOCK_FIELDS.issubset(self.locked_fields)

    @property
    def stable_id(self) -> str:
        return content_id(
            "comparison-lock",
            {
                "enabled": self.enabled,
                "group_id": self.group_id,
                "locked_fields": sorted(self.locked_fields),
                "method_specific_overrides_forbidden": self.method_specific_overrides_forbidden,
            },
        )


@dataclass(frozen=True, slots=True)
class RenderConfigSummary:
    config_id: str
    purpose: RenderPurpose
    camera_path_id: str
    channels: tuple[RenderChannel, ...]
    comparison_lock: ComparisonLock
    statistical_non_physical_label: bool
    future_frame_access: bool

    def __post_init__(self) -> None:
        if not self.config_id:
            raise ValueError("config_id must not be empty")
        if not self.camera_path_id:
            raise ValueError("camera_path_id must not be empty")
        if not self.channels:
            raise ValueError("at least one render channel is required")
        if len(set(self.channels)) != len(self.channels):
            raise ValueError("render channels must be unique")
        if not self.statistical_non_physical_label:
            raise ValueError("statistical display particles must be labeled non-physical")
        if self.future_frame_access:
            raise ValueError("render configurations may not use future frames")
        if self.purpose in {RenderPurpose.SHARED_COMPARISON, RenderPurpose.HERO}:
            if not self.comparison_lock.is_primary_ready:
                raise ValueError("primary/hero configurations require a complete comparison lock")

    @property
    def stable_id(self) -> str:
        return content_id(
            "render-config",
            {
                "config_id": self.config_id,
                "purpose": self.purpose,
                "camera_path_id": self.camera_path_id,
                "channels": self.channels,
                "comparison_lock": self.comparison_lock,
                "statistical_non_physical_label": self.statistical_non_physical_label,
                "future_frame_access": self.future_frame_access,
            },
        )


@dataclass(frozen=True, slots=True)
class RenderArtifactInput:
    kind: str
    path: PurePosixPath
    schema_version: str
    sha256: str

    def __post_init__(self) -> None:
        if not self.kind:
            raise ValueError("artifact kind must not be empty")
        if self.path.is_absolute():
            raise ValueError("artifact path must be relative")
        if not self.schema_version:
            raise ValueError("schema_version must not be empty")
        if len(self.sha256) != 64 or any(char not in "0123456789abcdef" for char in self.sha256):
            raise ValueError("sha256 must be a lowercase hexadecimal digest")


@dataclass(frozen=True, slots=True)
class RenderPlan:
    config_id: str
    mode: RenderPurpose
    scene_id: str
    output: Mapping[str, object]
    schedule: FrameSchedule
    camera: Mapping[str, object]
    layers: tuple[Mapping[str, object], ...]
    display_policy: Mapping[str, object]
    comparison_lock: ComparisonLock
    postprocess: Mapping[str, object]
    evidence: Mapping[str, object]
    raw: Mapping[str, object]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> RenderPlan:
        required = {
            "config_id",
            "mode",
            "scene_id",
            "output",
            "timeline",
            "camera",
            "layers",
            "display_policy",
            "comparison_lock",
            "postprocess",
            "evidence",
        }
        missing = required - payload.keys()
        if missing:
            raise ValueError(f"missing render config keys: {sorted(missing)}")

        timeline = _mapping(payload["timeline"], "timeline")
        output = _mapping(payload["output"], "output")
        camera = _mapping(payload["camera"], "camera")
        display_policy = _mapping(payload["display_policy"], "display_policy")
        comparison = _mapping(payload["comparison_lock"], "comparison_lock")
        postprocess = _mapping(payload["postprocess"], "postprocess")
        evidence = _mapping(payload["evidence"], "evidence")
        layers_raw = payload["layers"]
        if not isinstance(layers_raw, Sequence) or isinstance(layers_raw, (str, bytes)):
            raise ValueError("layers must be a sequence")
        layers = tuple(_mapping(layer, "layer") for layer in layers_raw)

        if display_policy.get("physics_camera_decoupled") is not True:
            raise ValueError("physics and camera policies must remain decoupled")
        statistical = _mapping(display_policy["statistical_particles"], "statistical_particles")
        if statistical.get("non_physical_label") is not True:
            raise ValueError("statistical display particles must be labeled non-physical")
        if postprocess.get("future_frame_access") is not False:
            raise ValueError("future-frame post-processing is forbidden")

        lock = ComparisonLock(
            enabled=bool(comparison["enabled"]),
            group_id=str(comparison["group_id"]),
            locked_fields=tuple(str(item) for item in comparison["lock_fields"]),
            method_specific_overrides_forbidden=bool(
                comparison["method_specific_overrides_forbidden"]
            ),
        )
        mode = RenderPurpose(str(payload["mode"]))
        if (
            mode in {RenderPurpose.SHARED_COMPARISON, RenderPurpose.HERO}
            and not lock.is_primary_ready
        ):
            raise ValueError("shared-comparison and hero plans require a complete comparison lock")

        paths = camera.get("paths")
        if not isinstance(paths, Sequence) or isinstance(paths, (str, bytes)) or not paths:
            raise ValueError("camera.paths must be a non-empty sequence")

        plan = cls(
            config_id=str(payload["config_id"]),
            mode=mode,
            scene_id=str(payload["scene_id"]),
            output=output,
            schedule=FrameSchedule(
                start_time=float(timeline["start_time"]),
                end_time=float(timeline["end_time"]),
                sample_interval=float(timeline["sample_interval"]),
            ),
            camera=camera,
            layers=layers,
            display_policy=display_policy,
            comparison_lock=lock,
            postprocess=postprocess,
            evidence=evidence,
            raw=dict(payload),
        )
        if plan.schedule.frame_count < 1:
            raise ValueError("render plan must contain at least one frame")
        if int(output["width"]) <= 0 or int(output["height"]) <= 0:
            raise ValueError("output dimensions must be positive")
        return plan

    @property
    def camera_path_ids(self) -> tuple[str, ...]:
        paths = self.camera["paths"]
        assert isinstance(paths, Sequence) and not isinstance(paths, (str, bytes))
        return tuple(str(_mapping(path, "camera path")["path_ref"]) for path in paths)

    @property
    def camera_path_rows(self) -> tuple[dict[str, str], ...]:
        paths = self.camera["paths"]
        assert isinstance(paths, Sequence) and not isinstance(paths, (str, bytes))
        rows: list[dict[str, str]] = []
        for raw_path in paths:
            path = _mapping(raw_path, "camera path")
            digest = str(path["sha256"])
            if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
                raise ValueError("camera path sha256 must be a lowercase hexadecimal digest")
            rows.append({"path_ref": str(path["path_ref"]), "sha256": digest})
        return tuple(rows)

    @property
    def camera_shot_ids(self) -> tuple[str, ...]:
        """Return stable shot identifiers declared by the render plan.

        Camera-path files own interpolation details, while the scene render
        config owns the paper/video shot identity.  Keeping both in the
        manifest lets a final frame be traced back to a storyboard shot
        without teaching the renderer about any particular Hero Scene.
        """

        paths = self.camera["paths"]
        assert isinstance(paths, Sequence) and not isinstance(paths, (str, bytes))
        return tuple(str(_mapping(path, "camera path")["shot_id"]) for path in paths)

    @property
    def channels(self) -> tuple[RenderChannel, ...]:
        channels: list[RenderChannel] = []
        for layer in self.layers:
            if bool(layer.get("enabled", True)):
                channels.append(RenderChannel(str(layer["kind"])))
        return tuple(channels)

    @property
    def config_digest(self) -> str:
        return content_id("render-config", self.raw)

    @property
    def summary(self) -> RenderConfigSummary:
        statistical = _mapping(
            self.display_policy["statistical_particles"], "statistical_particles"
        )
        return RenderConfigSummary(
            config_id=self.config_id,
            purpose=self.mode,
            camera_path_id=self.camera_path_ids[0],
            channels=self.channels,
            comparison_lock=self.comparison_lock,
            statistical_non_physical_label=bool(statistical["non_physical_label"]),
            future_frame_access=bool(self.postprocess["future_frame_access"]),
        )


def _mapping(value: object, name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def render_summary_from_mapping(payload: Mapping[str, object]) -> RenderConfigSummary:
    return RenderPlan.from_mapping(payload).summary


def comparison_lock_digest(payload: Mapping[str, object]) -> str:
    comparison = _mapping(payload["comparison_lock"], "comparison_lock")
    fields = comparison["lock_fields"]
    if not isinstance(fields, Sequence) or isinstance(fields, (str, bytes)):
        raise ValueError("comparison_lock.lock_fields must be a sequence")
    locked_payload = {str(field): payload[str(field)] for field in fields}
    return content_id(
        "comparison-lock",
        {
            "group_id": comparison["group_id"],
            "method_specific_overrides_forbidden": comparison[
                "method_specific_overrides_forbidden"
            ],
            "values": locked_payload,
        },
    )


def build_render_manifest(
    plan: RenderPlan,
    artifacts: Sequence[ArtifactRef],
    *,
    renderer_name: str,
    renderer_version: str,
    evidence_links: Mapping[str, object] | None = None,
) -> dict[str, object]:
    artifact_rows = sorted(
        (
            {
                "kind": artifact.kind,
                "path": artifact.path.as_posix(),
                "schema_version": artifact.schema_version,
                "sha256": artifact.content_sha256,
            }
            for artifact in artifacts
        ),
        key=lambda row: (str(row["kind"]), str(row["path"])),
    )
    all_hashed = all(
        isinstance(row["sha256"], str) and len(row["sha256"]) == 64
        for row in artifact_rows
    )
    metric_artifact_paths = sorted(
        str(row["path"])
        for row in artifact_rows
        if str(row["kind"]) == "metrics-report"
    )

    links: dict[str, object] = {
        "case_id": None,
        "shot_ids": list(plan.camera_shot_ids),
        "run_ids": [],
        "claim_ids": [],
        "metric_artifact_paths": metric_artifact_paths,
    }
    if evidence_links is not None:
        unknown = set(evidence_links) - set(links)
        if unknown:
            raise ValueError(f"unknown render evidence-link fields: {sorted(unknown)}")
        links.update(evidence_links)
    links["complete"] = _evidence_links_complete(links)

    lock_digest = comparison_lock_digest(plan.raw) if plan.comparison_lock.enabled else None
    renderer_digest = content_id(
        "renderer",
        {"name": renderer_name, "version": renderer_version},
    )
    manifest_core: dict[str, object] = {
        "schema_version": "1.0.0",
        "renderer": {
            "name": renderer_name,
            "version": renderer_version,
            "digest": renderer_digest,
        },
        "config": {
            "config_id": plan.config_id,
            "mode": plan.mode.value,
            "scene_id": plan.scene_id,
            "digest": plan.config_digest,
            "display_policy_digest": content_id(
                "display-policy",
                plan.display_policy,
            ),
            "comparison_lock_digest": lock_digest,
        },
        "timeline": {
            "start_time": plan.schedule.start_time,
            "end_time": plan.schedule.end_time,
            "sample_interval": plan.schedule.sample_interval,
            "frame_count": plan.schedule.frame_count,
        },
        "camera": {
            "projection": plan.camera["projection"],
            "paths": list(plan.camera_path_rows),
        },
        "artifacts": artifact_rows,
        "evidence_links": links,
        "output": {
            "width": plan.output["width"],
            "height": plan.output["height"],
            "fps": plan.output["fps"],
            "frame_format": plan.output["frame_format"],
            "color_space": plan.output["color_space"],
            "alpha": plan.output["alpha"],
        },
        "evidence": {
            "all_artifacts_hashed": all_hashed,
            "physics_camera_decoupled": plan.display_policy["physics_camera_decoupled"],
            "method_specific_overrides_forbidden": (
                plan.comparison_lock.method_specific_overrides_forbidden
            ),
            "require_run_ids": plan.evidence["require_run_ids"],
            "require_artifact_hashes": plan.evidence["require_artifact_hashes"],
            "require_renderer_hash": plan.evidence["require_renderer_hash"],
            "require_metric_links": plan.evidence["require_metric_links"],
        },
        "physics_state_mutated": False,
    }
    return {"render_id": content_id("render", manifest_core), **manifest_core}


def _evidence_links_complete(links: Mapping[str, object]) -> bool:
    case_id = links.get("case_id")
    shot_ids = links.get("shot_ids")
    run_ids = links.get("run_ids")
    claim_ids = links.get("claim_ids")
    metric_paths = links.get("metric_artifact_paths")
    return (
        isinstance(case_id, str)
        and bool(case_id)
        and _non_empty_string_sequence(shot_ids)
        and _non_empty_string_sequence(run_ids)
        and _non_empty_string_sequence(claim_ids)
        and _non_empty_string_sequence(metric_paths)
    )


def _non_empty_string_sequence(value: object) -> bool:
    return (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes))
        and bool(value)
        and all(isinstance(item, str) and bool(item) for item in value)
    )


def write_manifest(path: Path, manifest: Mapping[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    path.write_text(payload, encoding="utf-8")
    return path


def manifest_canonical_json(manifest: Mapping[str, object]) -> str:
    return canonical_json(manifest)
