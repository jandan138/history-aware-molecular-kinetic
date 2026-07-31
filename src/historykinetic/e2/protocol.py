from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from historykinetic.echo.protocol import EchoE1Protocol, load_echo_protocol


@dataclass(frozen=True, order=True, slots=True)
class MoleculeBudget:
    maximum_component_size: int
    maximum_cycle_rank: int

    def __post_init__(self) -> None:
        if self.maximum_component_size < 2 or self.maximum_cycle_rank < 0:
            raise ValueError("invalid molecule budget")

    @property
    def branch_name(self) -> str:
        return (
            f"budget-l{self.maximum_component_size}"
            f"-g{self.maximum_cycle_rank}"
        )


@dataclass(frozen=True, slots=True)
class E2AcceptanceSpec:
    minimum_reverse_ladder_spearman: float
    minimum_reverse_full_ghost_gap: float
    minimum_selected_random_gap: float
    minimum_selected_topology_gap: float
    minimum_control_gap_ci_lower: float
    maximum_control_dose_relative_error: float
    maximum_forward_recovery: float


@dataclass(frozen=True, slots=True)
class E2RenderSpec:
    hero_particle_count: int
    hero_seed: int
    fps: int
    frame_repeat: int
    final_hold_frames: int


@dataclass(frozen=True, slots=True)
class MolecularEchoesE2Protocol:
    schema_version: str
    study_id: str
    e1_protocol: EchoE1Protocol
    e1_protocol_path: Path
    layer_width: float
    budgets: tuple[MoleculeBudget, ...]
    selected_budget: MoleculeBudget
    seeds: tuple[int, ...]
    calibration_particle_count: int
    calibration_seeds: tuple[int, ...]
    random_seed_offset: int
    topology_seed_offset: int
    bootstrap_resamples: int
    bootstrap_seed: int
    acceptance: E2AcceptanceSpec
    render: E2RenderSpec

    def __post_init__(self) -> None:
        if not self.schema_version or not self.study_id:
            raise ValueError("schema_version and study_id must not be empty")
        if self.layer_width <= 0:
            raise ValueError("layer_width must be positive")
        if not self.budgets or len(set(self.budgets)) != len(self.budgets):
            raise ValueError("budgets must be non-empty and unique")
        if self.selected_budget not in self.budgets:
            raise ValueError("selected control budget must be in the budget ladder")
        if self.seeds != self.e1_protocol.seeds:
            raise ValueError("E2 primary seeds must inherit the frozen E1 seeds")
        if set(self.calibration_seeds) & set(self.seeds):
            raise ValueError("calibration seeds must be excluded from primary evidence")
        registered_counts = {size.count for size in self.e1_protocol.sizes}
        if self.calibration_particle_count not in registered_counts:
            raise ValueError("calibration size must be an E1 registered particle count")
        if self.render.hero_particle_count not in registered_counts:
            raise ValueError("hero size must be registered")
        if self.render.hero_seed not in self.seeds:
            raise ValueError("hero seed must be a primary seed")
        if self.bootstrap_resamples < 100:
            raise ValueError("bootstrap requires at least 100 resamples")

    @property
    def branch_names(self) -> tuple[str, ...]:
        return (
            "ghost",
            *(budget.branch_name for budget in self.budgets),
            "full",
            "count-time-matched-random",
            f"topology-shuffled-{self.selected_budget.branch_name}",
        )


def load_e2_protocol(path: Path) -> MolecularEchoesE2Protocol:
    payload = _mapping(json.loads(path.read_text(encoding="utf-8")), "protocol")
    e1_path = (path.parent / str(payload["e1_protocol"])).resolve()
    e1 = load_echo_protocol(e1_path)
    molecule = _mapping(payload["molecule_ladder"], "molecule_ladder")
    control = _mapping(payload["controls"], "controls")
    calibration = _mapping(payload["calibration"], "calibration")
    bootstrap = _mapping(payload["bootstrap"], "bootstrap")
    acceptance = _mapping(payload["acceptance"], "acceptance")
    render = _mapping(payload["render"], "render")
    budgets = tuple(
        MoleculeBudget(int(row[0]), int(row[1]))
        for row in _sequence(molecule["budgets"], "molecule_ladder.budgets")
    )
    selected_raw = _sequence(
        molecule["selected_control_budget"],
        "molecule_ladder.selected_control_budget",
    )
    return MolecularEchoesE2Protocol(
        schema_version=str(payload["schema_version"]),
        study_id=str(payload["study_id"]),
        e1_protocol=e1,
        e1_protocol_path=e1_path,
        layer_width=float(payload["layer_width"]),
        budgets=budgets,
        selected_budget=MoleculeBudget(int(selected_raw[0]), int(selected_raw[1])),
        seeds=tuple(int(seed) for seed in _sequence(payload["seeds"], "seeds")),
        calibration_particle_count=int(calibration["particle_count"]),
        calibration_seeds=tuple(
            int(seed) for seed in _sequence(calibration["excluded_seeds"], "excluded_seeds")
        ),
        random_seed_offset=int(control["random_seed_offset"]),
        topology_seed_offset=int(control["topology_seed_offset"]),
        bootstrap_resamples=int(bootstrap["resamples"]),
        bootstrap_seed=int(bootstrap["seed"]),
        acceptance=E2AcceptanceSpec(
            **{key: float(value) for key, value in acceptance.items()}
        ),
        render=E2RenderSpec(
            hero_particle_count=int(render["hero_particle_count"]),
            hero_seed=int(render["hero_seed"]),
            fps=int(render["fps"]),
            frame_repeat=int(render["frame_repeat"]),
            final_hold_frames=int(render["final_hold_frames"]),
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
