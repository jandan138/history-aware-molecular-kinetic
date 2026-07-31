from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from math import isclose
from pathlib import Path
from typing import Any

from historykinetic.solvers import BoundaryKind, Domain2D


class EchoBranchKind(StrEnum):
    FORWARD = "forward"
    EXACT_REVERSE = "exact_reverse"
    CHAOTIZED_REVERSE = "chaotized_reverse"
    DSMC_REVERSE = "dsmc_reverse"
    GHOST = "ghost"


@dataclass(frozen=True, slots=True)
class ParticleSize:
    count: int
    diameter: float

    def __post_init__(self) -> None:
        if self.count < 2:
            raise ValueError("particle count must be at least two")
        if self.diameter <= 0:
            raise ValueError("particle diameter must be positive")


@dataclass(frozen=True, slots=True)
class PatternSpec:
    foreground_vertical: tuple[float, float, float, float]
    foreground_horizontal_x: tuple[float, float]
    foreground_horizontal_y_bands: tuple[tuple[float, float], ...]

    def contains(self, position: tuple[float, float]) -> bool:
        x, y = position
        x0, x1, y0, y1 = self.foreground_vertical
        vertical = x0 <= x <= x1 and y0 <= y <= y1
        hx0, hx1 = self.foreground_horizontal_x
        horizontal = hx0 <= x <= hx1 and any(
            low <= y <= high for low, high in self.foreground_horizontal_y_bands
        )
        return vertical or horizontal


@dataclass(frozen=True, slots=True)
class AcceptanceSpec:
    maximum_position_rms: float
    maximum_velocity_rms: float
    maximum_pivot_color_score: float
    minimum_exact_terminal_color_score: float
    minimum_changed_particle_fraction: float
    maximum_construction_tv: float
    maximum_invariant_mismatch: float
    minimum_mean_echo_gap: float
    minimum_echo_gap_ci_lower: float


@dataclass(frozen=True, slots=True)
class RenderSpec:
    hero_particle_count: int
    hero_seed: int
    fps: int
    frame_repeat: int
    final_hold_frames: int
    foreground_color: str
    background_color: str


@dataclass(frozen=True, slots=True)
class EchoE1Protocol:
    schema_version: str
    study_id: str
    domain: Domain2D
    particle_mass: float
    sizes: tuple[ParticleSize, ...]
    temperature: float
    temperature_x: float
    temperature_y: float
    mean_velocity: tuple[float, float]
    pattern: PatternSpec
    preparation_time: float
    future_horizon: float
    sample_interval: float
    seeds: tuple[int, ...]
    chaotization_blocks: tuple[int, int]
    chaotization_seed_offset: int
    audit_spatial_grids: tuple[tuple[int, int], ...]
    audit_velocity_edges_standardized: tuple[tuple[float, ...], ...]
    dsmc_cells: tuple[int, int]
    dsmc_time_step: float
    dsmc_seed_offset: int
    bootstrap_resamples: int
    bootstrap_seed: int
    acceptance: AcceptanceSpec
    render: RenderSpec

    def __post_init__(self) -> None:
        if not self.schema_version or not self.study_id:
            raise ValueError("schema_version and study_id must not be empty")
        if self.domain.boundary is not BoundaryKind.PERIODIC:
            raise ValueError("E1 requires a periodic domain")
        if self.particle_mass <= 0:
            raise ValueError("particle mass must be positive")
        if self.temperature <= 0 or self.temperature_x <= 0 or self.temperature_y <= 0:
            raise ValueError("temperatures must be positive")
        if not isclose(
            0.5 * (self.temperature_x + self.temperature_y),
            self.temperature,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise ValueError("temperature must equal the mean of temperature_x/y")
        if self.preparation_time <= 0 or self.future_horizon <= 0 or self.sample_interval <= 0:
            raise ValueError("timing values must be positive")
        if not self.seeds or len(set(self.seeds)) != len(self.seeds):
            raise ValueError("seeds must be non-empty and unique")
        if self.chaotization_blocks not in self.audit_spatial_grids:
            raise ValueError("construction grid must be present in the audit grids")
        if self.render.hero_particle_count not in {size.count for size in self.sizes}:
            raise ValueError("hero_particle_count must be one of the registered sizes")
        if self.render.hero_seed not in self.seeds:
            raise ValueError("hero_seed must be one of the registered seeds")
        products = [size.count * size.diameter for size in self.sizes]
        if max(products) - min(products) > 1.0e-12:
            raise ValueError("registered E1 sizes must preserve N times diameter")

    def size_for_count(self, particle_count: int) -> ParticleSize:
        for size in self.sizes:
            if size.count == particle_count:
                return size
        raise KeyError(f"unregistered particle count: {particle_count}")


def load_echo_protocol(path: Path) -> EchoE1Protocol:
    payload = json.loads(path.read_text(encoding="utf-8"))
    root = _mapping(payload, "protocol")
    domain_raw = _mapping(root["domain"], "domain")
    particle_raw = _mapping(root["particle"], "particle")
    initial_raw = _mapping(root["initial"], "initial")
    pattern_raw = _mapping(root["pattern"], "pattern")
    timing_raw = _mapping(root["timing"], "timing")
    chaos_raw = _mapping(root["chaotization"], "chaotization")
    audit_raw = _mapping(root["audit"], "audit")
    dsmc_raw = _mapping(root["dsmc"], "dsmc")
    bootstrap_raw = _mapping(root["bootstrap"], "bootstrap")
    acceptance_raw = _mapping(root["acceptance"], "acceptance")
    render_raw = _mapping(root["render"], "render")

    if str(pattern_raw.get("kind")) != "analytic-e":
        raise ValueError("E1 v0 supports only the analytic-e passive-color pattern")

    protocol = EchoE1Protocol(
        schema_version=str(root["schema_version"]),
        study_id=str(root["study_id"]),
        domain=Domain2D(
            lower=_float_pair(domain_raw["lower"], "domain.lower"),
            upper=_float_pair(domain_raw["upper"], "domain.upper"),
            boundary=BoundaryKind(str(domain_raw["boundary"])),
        ),
        particle_mass=float(particle_raw["mass"]),
        sizes=tuple(
            ParticleSize(count=int(row["count"]), diameter=float(row["diameter"]))
            for row in _mapping_sequence(particle_raw["sizes"], "particle.sizes")
        ),
        temperature=float(initial_raw["temperature"]),
        temperature_x=float(initial_raw["temperature_x"]),
        temperature_y=float(initial_raw["temperature_y"]),
        mean_velocity=_float_pair(initial_raw["mean_velocity"], "initial.mean_velocity"),
        pattern=PatternSpec(
            foreground_vertical=_float_quad(
                pattern_raw["foreground_vertical"], "pattern.foreground_vertical"
            ),
            foreground_horizontal_x=_float_pair(
                pattern_raw["foreground_horizontal_x"], "pattern.foreground_horizontal_x"
            ),
            foreground_horizontal_y_bands=tuple(
                _float_pair(row, "pattern.foreground_horizontal_y_bands row")
                for row in _sequence(
                    pattern_raw["foreground_horizontal_y_bands"],
                    "pattern.foreground_horizontal_y_bands",
                )
            ),
        ),
        preparation_time=float(timing_raw["preparation_time"]),
        future_horizon=float(timing_raw["future_horizon"]),
        sample_interval=float(timing_raw["sample_interval"]),
        seeds=tuple(int(seed) for seed in _sequence(root["seeds"], "seeds")),
        chaotization_blocks=(
            int(chaos_raw["blocks_x"]),
            int(chaos_raw["blocks_y"]),
        ),
        chaotization_seed_offset=int(chaos_raw["seed_offset"]),
        audit_spatial_grids=tuple(
            _int_pair(row, "audit.spatial_grids row")
            for row in _sequence(audit_raw["spatial_grids"], "audit.spatial_grids")
        ),
        audit_velocity_edges_standardized=tuple(
            tuple(float(edge) for edge in _sequence(row, "velocity edge row"))
            for row in _sequence(
                audit_raw["velocity_edges_standardized"],
                "audit.velocity_edges_standardized",
            )
        ),
        dsmc_cells=(int(dsmc_raw["cells_x"]), int(dsmc_raw["cells_y"])),
        dsmc_time_step=float(dsmc_raw["time_step"]),
        dsmc_seed_offset=int(dsmc_raw["seed_offset"]),
        bootstrap_resamples=int(bootstrap_raw["resamples"]),
        bootstrap_seed=int(bootstrap_raw["seed"]),
        acceptance=AcceptanceSpec(
            **{key: float(value) for key, value in acceptance_raw.items()}
        ),
        render=RenderSpec(
            hero_particle_count=int(render_raw["hero_particle_count"]),
            hero_seed=int(render_raw["hero_seed"]),
            fps=int(render_raw["fps"]),
            frame_repeat=int(render_raw["frame_repeat"]),
            final_hold_frames=int(render_raw["final_hold_frames"]),
            foreground_color=str(render_raw["foreground_color"]),
            background_color=str(render_raw["background_color"]),
        ),
    )
    return protocol


def _mapping(value: object, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _sequence(value: object, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be an array")
    return value


def _mapping_sequence(value: object, name: str) -> list[dict[str, Any]]:
    rows = _sequence(value, name)
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{name} must contain objects")
    return rows


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


def _float_quad(value: object, name: str) -> tuple[float, float, float, float]:
    row = _sequence(value, name)
    if len(row) != 4:
        raise ValueError(f"{name} must contain four numbers")
    return (float(row[0]), float(row[1]), float(row[2]), float(row[3]))
