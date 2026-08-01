"""Frozen E4 causal-steering recipe contract."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from historykinetic.echo.protocol import EchoE1Protocol, load_echo_protocol


@dataclass(frozen=True, slots=True)
class E4HeroSpec:
    particle_count: int
    seed: int
    target_id: str
    target_description: str
    target_x_bounds: tuple[float, float]
    target_y_bounds: tuple[float, float]
    expected_target_particle_ids: tuple[int, ...]
    expected_recommended_collision_ordinal: int
    expected_recommended_pair: tuple[int, int]
    expected_recommended_time: float
    recipe_tolerance: float


@dataclass(frozen=True, slots=True)
class E4RankingSpec:
    candidate_event_limit: int
    shortlist_size: int
    expected_shortlist_ordinals: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class E4AcceptanceSpec:
    minimum_target_ejection_fraction: float
    minimum_target_to_collateral_ratio: float
    minimum_baseline_event_reuse_fraction: float
    maximum_preview_median_seconds: float
    minimum_collision_pair_agreement: float
    maximum_collision_time_error: float
    maximum_terminal_position_rms: float
    maximum_terminal_velocity_rms: float
    maximum_edit_momentum_error: float
    maximum_edit_energy_error: float


@dataclass(frozen=True, slots=True)
class E4RenderSpec:
    fps: int
    frame_repeat: int
    final_hold_frames: int
    foreground_color: str
    background_color: str
    target_color: str
    selected_color: str
    causal_cone_color: str


@dataclass(frozen=True, slots=True)
class MolecularTimeMachineE4Protocol:
    schema_version: str
    study_id: str
    e1_protocol: EchoE1Protocol
    e1_protocol_path: Path
    hero: E4HeroSpec
    ranking: E4RankingSpec
    fork_lead_time: float
    checkpoint_interval_events: int
    palette_angles_degrees: tuple[float, ...]
    end_time: float
    sample_interval: float
    acceptance: E4AcceptanceSpec
    render: E4RenderSpec

    def __post_init__(self) -> None:
        if not self.schema_version or not self.study_id:
            raise ValueError("schema_version and study_id must not be empty")
        if self.hero.particle_count not in {size.count for size in self.e1_protocol.sizes}:
            raise ValueError("E4 hero count must come from the frozen E1 protocol")
        if self.hero.seed not in self.e1_protocol.seeds:
            raise ValueError("E4 hero seed must come from the frozen E1 protocol")
        if self.ranking.candidate_event_limit <= 0 or self.ranking.shortlist_size <= 0:
            raise ValueError("E4 ranking limits must be positive")
        if self.ranking.shortlist_size > self.ranking.candidate_event_limit:
            raise ValueError("E4 shortlist cannot exceed candidate event limit")
        if not self.palette_angles_degrees or len(set(self.palette_angles_degrees)) != len(
            self.palette_angles_degrees
        ):
            raise ValueError("E4 palette angles must be non-empty and unique")
        if self.fork_lead_time <= 0 or self.checkpoint_interval_events <= 0:
            raise ValueError("E4 fork lead time and checkpoint interval must be positive")
        if self.end_time <= 0 or self.sample_interval <= 0:
            raise ValueError("E4 measurement times must be positive")
        if self.hero.target_x_bounds[0] >= self.hero.target_x_bounds[1]:
            raise ValueError("E4 target x bounds must be ordered")
        if self.hero.target_y_bounds[0] >= self.hero.target_y_bounds[1]:
            raise ValueError("E4 target y bounds must be ordered")


def load_e4_protocol(path: Path) -> MolecularTimeMachineE4Protocol:
    payload = _mapping(json.loads(path.read_text(encoding="utf-8")), "protocol")
    e1_path = (path.parent / str(payload["e1_protocol"])).resolve()
    hero = _mapping(payload["hero"], "hero")
    target = _mapping(hero["target"], "hero.target")
    ranking = _mapping(payload["ranking"], "ranking")
    fork = _mapping(payload["fork"], "fork")
    palette = _mapping(payload["palette"], "palette")
    measurement = _mapping(payload["measurement"], "measurement")
    acceptance = _mapping(payload["acceptance"], "acceptance")
    render = _mapping(payload["render"], "render")
    expected_pair = _sequence(hero["expected_recommended_pair"], "hero.expected_recommended_pair")
    return MolecularTimeMachineE4Protocol(
        schema_version=str(payload["schema_version"]),
        study_id=str(payload["study_id"]),
        e1_protocol=load_echo_protocol(e1_path),
        e1_protocol_path=e1_path,
        hero=E4HeroSpec(
            particle_count=int(hero["particle_count"]),
            seed=int(hero["seed"]),
            target_id=str(target["id"]),
            target_description=str(target["description"]),
            target_x_bounds=_float_pair(target["x_bounds"], "hero.target.x_bounds"),
            target_y_bounds=_float_pair(target["y_bounds"], "hero.target.y_bounds"),
            expected_target_particle_ids=tuple(
                int(value)
                for value in _sequence(
                    target["expected_foreground_particle_ids"],
                    "hero.target.expected_foreground_particle_ids",
                )
            ),
            expected_recommended_collision_ordinal=int(
                hero["expected_recommended_collision_ordinal"]
            ),
            expected_recommended_pair=(int(expected_pair[0]), int(expected_pair[1])),
            expected_recommended_time=float(hero["expected_recommended_time"]),
            recipe_tolerance=float(hero["recipe_tolerance"]),
        ),
        ranking=E4RankingSpec(
            candidate_event_limit=int(ranking["candidate_event_limit"]),
            shortlist_size=int(ranking["shortlist_size"]),
            expected_shortlist_ordinals=tuple(
                int(value)
                for value in _sequence(
                    ranking["expected_shortlist_ordinals"],
                    "ranking.expected_shortlist_ordinals",
                )
            ),
        ),
        fork_lead_time=float(fork["lead_time"]),
        checkpoint_interval_events=int(fork["checkpoint_interval_events"]),
        palette_angles_degrees=tuple(
            float(value) for value in _sequence(palette["angles_degrees"], "palette.angles_degrees")
        ),
        end_time=float(measurement["end_time"]),
        sample_interval=float(measurement["sample_interval"]),
        acceptance=E4AcceptanceSpec(**{key: float(value) for key, value in acceptance.items()}),
        render=E4RenderSpec(
            fps=int(render["fps"]),
            frame_repeat=int(render["frame_repeat"]),
            final_hold_frames=int(render["final_hold_frames"]),
            foreground_color=str(render["foreground_color"]),
            background_color=str(render["background_color"]),
            target_color=str(render["target_color"]),
            selected_color=str(render["selected_color"]),
            causal_cone_color=str(render["causal_cone_color"]),
        ),
    )


def _mapping(value: object, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _sequence(value: object, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be an array")
    return value


def _float_pair(value: object, name: str) -> tuple[float, float]:
    row = _sequence(value, name)
    if len(row) != 2:
        raise ValueError(f"{name} must contain two numbers")
    return (float(row[0]), float(row[1]))
