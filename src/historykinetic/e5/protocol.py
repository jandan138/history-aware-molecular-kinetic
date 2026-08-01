"""Frozen E5 Same Present, Chosen Future recipe contract."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from historykinetic.echo.protocol import EchoE1Protocol, load_echo_protocol


@dataclass(frozen=True, slots=True)
class E5TargetSpec:
    target_id: str
    description: str
    x_bounds: tuple[float, float]
    x_lower_inclusive: bool
    y_bounds: tuple[float, float]
    expected_foreground_particle_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class E5HeroSpec:
    particle_count: int
    seed: int
    pivot_time: float
    target: E5TargetSpec
    expected_selected_swaps: tuple[tuple[int, int], ...]
    expected_preview_count: int
    recipe_tolerance: float


@dataclass(frozen=True, slots=True)
class E5SurgerySpec:
    declared_spatial_grid: tuple[int, int]
    maximum_disjoint_swaps: int


@dataclass(frozen=True, slots=True)
class E5AcceptanceSpec:
    minimum_target_ejection_fraction: float
    minimum_target_region_reduction_fraction: float
    minimum_collateral_retention_fraction: float
    maximum_touched_particle_count: int
    maximum_pivot_replay_position_rms: float
    maximum_pivot_replay_velocity_rms: float
    maximum_mass_error: float
    maximum_momentum_error: float
    maximum_energy_error: float


@dataclass(frozen=True, slots=True)
class E5RenderSpec:
    fps: int
    frame_repeat: int
    final_hold_frames: int
    foreground_color: str
    background_color: str
    target_color: str
    selected_color: str
    surgery_color: str


@dataclass(frozen=True, slots=True)
class MolecularTimeMachineE5Protocol:
    schema_version: str
    study_id: str
    e1_protocol: EchoE1Protocol
    e1_protocol_path: Path
    hero: E5HeroSpec
    surgery: E5SurgerySpec
    end_time: float
    sample_interval: float
    acceptance: E5AcceptanceSpec
    render: E5RenderSpec

    def __post_init__(self) -> None:
        if not self.schema_version or not self.study_id:
            raise ValueError("schema_version and study_id must not be empty")
        if self.hero.particle_count not in {size.count for size in self.e1_protocol.sizes}:
            raise ValueError("E5 hero count must come from the frozen E1 protocol")
        if self.hero.seed not in self.e1_protocol.seeds:
            raise ValueError("E5 hero seed must come from the frozen E1 protocol")
        if not 0.0 < self.hero.pivot_time < self.end_time:
            raise ValueError("E5 pivot must lie inside the measured future")
        if self.sample_interval <= 0.0:
            raise ValueError("E5 sample interval must be positive")
        if self.hero.target.x_bounds[0] >= self.hero.target.x_bounds[1]:
            raise ValueError("E5 target x bounds must be ordered")
        if self.hero.target.y_bounds[0] >= self.hero.target.y_bounds[1]:
            raise ValueError("E5 target y bounds must be ordered")
        if not self.hero.target.expected_foreground_particle_ids:
            raise ValueError("E5 expected target membership must not be empty")
        blocks_x, blocks_y = self.surgery.declared_spatial_grid
        if blocks_x <= 0 or blocks_y <= 0:
            raise ValueError("E5 declared spatial grid must be positive")
        if self.surgery.maximum_disjoint_swaps not in (1, 2):
            raise ValueError("E5 v0 supports one or two disjoint swaps")
        if self.hero.expected_preview_count <= 0:
            raise ValueError("E5 expected preview count must be positive")


def load_e5_protocol(path: Path) -> MolecularTimeMachineE5Protocol:
    payload = _mapping(json.loads(path.read_text(encoding="utf-8")), "protocol")
    e1_path = (path.parent / str(payload["e1_protocol"])).resolve()
    hero = _mapping(payload["hero"], "hero")
    target = _mapping(hero["target"], "hero.target")
    surgery = _mapping(payload["surgery"], "surgery")
    measurement = _mapping(payload["measurement"], "measurement")
    acceptance = _mapping(payload["acceptance"], "acceptance")
    render = _mapping(payload["render"], "render")
    return MolecularTimeMachineE5Protocol(
        schema_version=str(payload["schema_version"]),
        study_id=str(payload["study_id"]),
        e1_protocol=load_echo_protocol(e1_path),
        e1_protocol_path=e1_path,
        hero=E5HeroSpec(
            particle_count=int(hero["particle_count"]),
            seed=int(hero["seed"]),
            pivot_time=float(hero["pivot_time"]),
            target=E5TargetSpec(
                target_id=str(target["id"]),
                description=str(target["description"]),
                x_bounds=_float_pair(target["x_bounds"], "hero.target.x_bounds"),
                x_lower_inclusive=bool(target["x_lower_inclusive"]),
                y_bounds=_float_pair(target["y_bounds"], "hero.target.y_bounds"),
                expected_foreground_particle_ids=tuple(
                    int(value)
                    for value in _sequence(
                        target["expected_foreground_particle_ids"],
                        "hero.target.expected_foreground_particle_ids",
                    )
                ),
            ),
            expected_selected_swaps=tuple(
                _int_pair(row, "hero.expected_selected_swaps row")
                for row in _sequence(
                    hero["expected_selected_swaps"], "hero.expected_selected_swaps"
                )
            ),
            expected_preview_count=int(hero["expected_preview_count"]),
            recipe_tolerance=float(hero["recipe_tolerance"]),
        ),
        surgery=E5SurgerySpec(
            declared_spatial_grid=_int_pair(
                surgery["declared_spatial_grid"], "surgery.declared_spatial_grid"
            ),
            maximum_disjoint_swaps=int(surgery["maximum_disjoint_swaps"]),
        ),
        end_time=float(measurement["end_time"]),
        sample_interval=float(measurement["sample_interval"]),
        acceptance=E5AcceptanceSpec(
            minimum_target_ejection_fraction=float(
                acceptance["minimum_target_ejection_fraction"]
            ),
            minimum_target_region_reduction_fraction=float(
                acceptance["minimum_target_region_reduction_fraction"]
            ),
            minimum_collateral_retention_fraction=float(
                acceptance["minimum_collateral_retention_fraction"]
            ),
            maximum_touched_particle_count=int(acceptance["maximum_touched_particle_count"]),
            maximum_pivot_replay_position_rms=float(
                acceptance["maximum_pivot_replay_position_rms"]
            ),
            maximum_pivot_replay_velocity_rms=float(
                acceptance["maximum_pivot_replay_velocity_rms"]
            ),
            maximum_mass_error=float(acceptance["maximum_mass_error"]),
            maximum_momentum_error=float(acceptance["maximum_momentum_error"]),
            maximum_energy_error=float(acceptance["maximum_energy_error"]),
        ),
        render=E5RenderSpec(
            fps=int(render["fps"]),
            frame_repeat=int(render["frame_repeat"]),
            final_hold_frames=int(render["final_hold_frames"]),
            foreground_color=str(render["foreground_color"]),
            background_color=str(render["background_color"]),
            target_color=str(render["target_color"]),
            selected_color=str(render["selected_color"]),
            surgery_color=str(render["surgery_color"]),
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


def _int_pair(value: object, name: str) -> tuple[int, int]:
    row = _sequence(value, name)
    if len(row) != 2:
        raise ValueError(f"{name} must contain two integers")
    return (int(row[0]), int(row[1]))
