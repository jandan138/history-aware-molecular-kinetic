from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from historykinetic.echo.protocol import EchoE1Protocol, load_echo_protocol


@dataclass(frozen=True, slots=True)
class E3HeroSpec:
    particle_count: int
    seed: int
    target_collision_ordinal: int
    expected_pair: tuple[int, int]
    expected_time: float
    recipe_tolerance: float


@dataclass(frozen=True, slots=True)
class E3AcceptanceSpec:
    minimum_baseline_terminal_color_score: float
    minimum_terminal_color_gap: float
    minimum_visibly_changed_fraction: float
    maximum_visibly_changed_fraction: float
    minimum_collision_pair_agreement: float
    maximum_collision_time_error: float
    maximum_terminal_position_rms: float
    maximum_terminal_velocity_rms: float
    maximum_edit_momentum_error: float
    maximum_edit_energy_error: float
    minimum_baseline_event_reuse_fraction: float
    maximum_peak_affected_fraction: float


@dataclass(frozen=True, slots=True)
class E3RenderSpec:
    fps: int
    frame_repeat: int
    final_hold_frames: int
    foreground_color: str
    background_color: str
    edited_highlight_color: str
    causal_cone_color: str


@dataclass(frozen=True, slots=True)
class MolecularTimeMachineE3Protocol:
    schema_version: str
    study_id: str
    e1_protocol: EchoE1Protocol
    e1_protocol_path: Path
    hero: E3HeroSpec
    fork_lead_time: float
    checkpoint_interval_events: int
    edit_angle_degrees: float
    end_time: float
    sample_interval: float
    visible_position_threshold: float
    acceptance: E3AcceptanceSpec
    render: E3RenderSpec

    def __post_init__(self) -> None:
        if not self.schema_version or not self.study_id:
            raise ValueError("schema_version and study_id must not be empty")
        if self.hero.particle_count not in {
            size.count for size in self.e1_protocol.sizes
        }:
            raise ValueError("E3 hero count must come from the frozen E1 protocol")
        if self.hero.seed not in self.e1_protocol.seeds:
            raise ValueError("E3 hero seed must come from the frozen E1 protocol")
        if self.fork_lead_time <= 0 or self.checkpoint_interval_events <= 0:
            raise ValueError("fork lead time and checkpoint interval must be positive")
        if self.end_time <= 0 or self.sample_interval <= 0:
            raise ValueError("measurement times must be positive")


def load_e3_protocol(path: Path) -> MolecularTimeMachineE3Protocol:
    payload = _mapping(json.loads(path.read_text(encoding="utf-8")), "protocol")
    e1_path = (path.parent / str(payload["e1_protocol"])).resolve()
    hero = _mapping(payload["hero"], "hero")
    fork = _mapping(payload["fork"], "fork")
    edit = _mapping(payload["edit"], "edit")
    measurement = _mapping(payload["measurement"], "measurement")
    acceptance = _mapping(payload["acceptance"], "acceptance")
    render = _mapping(payload["render"], "render")
    expected_pair = _sequence(hero["expected_pair"], "hero.expected_pair")
    return MolecularTimeMachineE3Protocol(
        schema_version=str(payload["schema_version"]),
        study_id=str(payload["study_id"]),
        e1_protocol=load_echo_protocol(e1_path),
        e1_protocol_path=e1_path,
        hero=E3HeroSpec(
            particle_count=int(hero["particle_count"]),
            seed=int(hero["seed"]),
            target_collision_ordinal=int(hero["target_collision_ordinal"]),
            expected_pair=(int(expected_pair[0]), int(expected_pair[1])),
            expected_time=float(hero["expected_time"]),
            recipe_tolerance=float(hero["recipe_tolerance"]),
        ),
        fork_lead_time=float(fork["lead_time"]),
        checkpoint_interval_events=int(fork["checkpoint_interval_events"]),
        edit_angle_degrees=float(edit["angle_degrees"]),
        end_time=float(measurement["end_time"]),
        sample_interval=float(measurement["sample_interval"]),
        visible_position_threshold=float(measurement["visible_position_threshold"]),
        acceptance=E3AcceptanceSpec(
            **{key: float(value) for key, value in acceptance.items()}
        ),
        render=E3RenderSpec(
            fps=int(render["fps"]),
            frame_repeat=int(render["frame_repeat"]),
            final_hold_frames=int(render["final_hold_frames"]),
            foreground_color=str(render["foreground_color"]),
            background_color=str(render["background_color"]),
            edited_highlight_color=str(render["edited_highlight_color"]),
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

