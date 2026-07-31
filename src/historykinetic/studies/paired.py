"""Paired EDMD-DSMC dataset construction for the Phase-I paper story."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from math import hypot, sqrt
from pathlib import Path
from typing import Any

from historykinetic.contracts import CollisionEvent
from historykinetic.graphs import summarize_history_window
from historykinetic.ids import canonical_json, content_id
from historykinetic.solvers import (
    BlockGrid,
    BoundaryKind,
    CircleObstacle,
    Domain2D,
    HardDiskDSMC,
    HardDiskEDMD,
    make_initial_state,
    observe_blocks,
    particle_count_from_packing_fraction,
)
from historykinetic.solvers.result import GeometryCollisionEvent


@dataclass(frozen=True, slots=True)
class PairedCase:
    case_id: str
    geometry_id: str
    state_id: str
    domain: Domain2D
    packing_fraction: float
    particle_radius: float
    particle_mass: float
    temperature: float
    mean_velocity: tuple[float, float]
    initial_kind: str
    stream_speed: float


@dataclass(frozen=True, slots=True)
class PairedStudyConfig:
    study_id: str
    cases: tuple[PairedCase, ...]
    seeds: tuple[int, ...]
    preparation_time: float
    end_time: float
    sample_interval: float
    future_horizon: float
    history_window: float
    blocks_x: int
    blocks_y: int
    dsmc_cells_x: int
    dsmc_cells_y: int
    dsmc_time_step: float
    minimum_block_samples: int
    ensemble_group_size: int

    def __post_init__(self) -> None:
        if not self.study_id or not self.cases or not self.seeds:
            raise ValueError("study_id, cases, and seeds must not be empty")
        if min(
            self.end_time,
            self.sample_interval,
            self.future_horizon,
            self.history_window,
            self.dsmc_time_step,
        ) <= 0:
            raise ValueError("study time scales must be positive")
        if self.preparation_time < 0:
            raise ValueError("preparation_time must be non-negative")
        ratio = self.future_horizon / self.sample_interval
        if abs(ratio - round(ratio)) > 1.0e-9:
            raise ValueError("future_horizon must be an integer multiple of sample_interval")
        if self.ensemble_group_size <= 0:
            raise ValueError("ensemble_group_size must be positive")
        if len(self.seeds) % self.ensemble_group_size != 0:
            raise ValueError("seed count must be divisible by ensemble_group_size")


@dataclass(frozen=True, slots=True)
class DiscrepancyRow:
    schema_version: str
    study_id: str
    case_id: str
    geometry_id: str
    state_id: str
    seed: int
    trajectory_group: str
    block_id: str
    time: float
    future_time: float
    state_features: dict[str, float]
    geometry_features: dict[str, float]
    numerical_features: dict[str, float]
    history_features: dict[str, float]
    feature_visibility: dict[str, str]
    targets: dict[str, float]
    paired_observables: dict[str, dict[str, float]]
    ensemble_members: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class PairedRunAudit:
    case_id: str
    seed: int
    particle_count: int
    exact_collision_count: int
    kinetic_collision_count: int
    exact_relative_energy_error: float
    kinetic_relative_energy_error: float
    exact_absolute_momentum_error: float
    kinetic_absolute_momentum_error: float
    row_count: int


@dataclass(frozen=True, slots=True)
class PairedStudyResult:
    config: PairedStudyConfig
    rows: tuple[DiscrepancyRow, ...]
    audits: tuple[PairedRunAudit, ...]


def load_study_config(path: Path) -> PairedStudyConfig:
    payload = json.loads(path.read_text(encoding="utf-8"))
    geometries = {
        str(row["geometry_id"]): _domain_from_mapping(row)
        for row in _sequence_of_mappings(payload["geometries"], "geometries")
    }
    states = {
        str(row["state_id"]): row
        for row in _sequence_of_mappings(payload["states"], "states")
    }
    cases: list[PairedCase] = []
    for raw_case in _sequence_of_mappings(payload["cases"], "cases"):
        geometry_id = str(raw_case["geometry_id"])
        state_id = str(raw_case["state_id"])
        raw_state = states[state_id]
        mean_velocity = _float_pair(raw_state["mean_velocity"], "mean_velocity")
        cases.append(
            PairedCase(
                case_id=str(raw_case["case_id"]),
                geometry_id=geometry_id,
                state_id=state_id,
                domain=geometries[geometry_id],
                packing_fraction=float(raw_state["packing_fraction"]),
                particle_radius=float(payload["particle"]["radius"]),
                particle_mass=float(payload["particle"]["mass"]),
                temperature=float(raw_state["temperature"]),
                mean_velocity=mean_velocity,
                initial_kind=str(raw_state["initial_kind"]),
                stream_speed=float(raw_state.get("stream_speed", 1.0)),
            )
        )
    sampling = _mapping(payload["sampling"], "sampling")
    partition = _mapping(payload["partition"], "partition")
    dsmc = _mapping(payload["dsmc"], "dsmc")
    return PairedStudyConfig(
        study_id=str(payload["study_id"]),
        cases=tuple(cases),
        seeds=tuple(int(seed) for seed in payload["seeds"]),
        preparation_time=float(sampling["preparation_time"]),
        end_time=float(sampling["end_time"]),
        sample_interval=float(sampling["sample_interval"]),
        future_horizon=float(sampling["future_horizon"]),
        history_window=float(sampling["history_window"]),
        blocks_x=int(partition["blocks_x"]),
        blocks_y=int(partition["blocks_y"]),
        dsmc_cells_x=int(dsmc["cells_x"]),
        dsmc_cells_y=int(dsmc["cells_y"]),
        dsmc_time_step=float(dsmc["time_step"]),
        minimum_block_samples=int(sampling["minimum_block_samples"]),
        ensemble_group_size=int(sampling["ensemble_group_size"]),
    )


def run_paired_study(config: PairedStudyConfig) -> PairedStudyResult:
    rows: list[DiscrepancyRow] = []
    audits: list[PairedRunAudit] = []
    for case in config.cases:
        for seed in config.seeds:
            case_rows, audit = _run_case_seed(config, case, seed)
            rows.extend(case_rows)
            audits.append(audit)
    aggregated = _aggregate_seed_ensembles(rows, config)
    return PairedStudyResult(config=config, rows=tuple(aggregated), audits=tuple(audits))


def _run_case_seed(
    config: PairedStudyConfig,
    case: PairedCase,
    seed: int,
) -> tuple[list[DiscrepancyRow], PairedRunAudit]:
    observation_domain = Domain2D(
        lower=case.domain.lower,
        upper=case.domain.upper,
        boundary=BoundaryKind.REFLECTIVE,
    )
    grid = BlockGrid(observation_domain, config.blocks_x, config.blocks_y)
    particle_count = particle_count_from_packing_fraction(
        observation_domain,
        radius=case.particle_radius,
        packing_fraction=case.packing_fraction,
    )
    initial_state = make_initial_state(
        case.domain,
        particle_count=particle_count,
        radius=case.particle_radius,
        mass=case.particle_mass,
        temperature=case.temperature,
        mean_velocity=case.mean_velocity,
        seed=seed,
        kind=case.initial_kind,
        stream_speed=case.stream_speed,
    )
    preparation = HardDiskEDMD(case.domain, block_locator=grid.block_id).run(
        initial_state,
        end_time=max(config.preparation_time, config.sample_interval),
        sample_interval=max(config.preparation_time, config.sample_interval),
    )
    prepared_state = (
        preparation.snapshots[-1].state
        if config.preparation_time > 0
        else initial_state
    )
    exact = HardDiskEDMD(observation_domain, block_locator=grid.block_id).run(
        prepared_state,
        end_time=config.end_time,
        sample_interval=config.sample_interval,
    )
    kinetic = HardDiskDSMC(
        observation_domain,
        cells_x=config.dsmc_cells_x,
        cells_y=config.dsmc_cells_y,
        time_step=config.dsmc_time_step,
        seed=_kinetic_seed(case.case_id, seed),
        block_locator=grid.block_id,
    ).run(
        prepared_state,
        end_time=config.end_time,
        sample_interval=config.sample_interval,
    )
    if len(exact.snapshots) != len(kinetic.snapshots):
        raise RuntimeError("paired solvers emitted different snapshot counts")

    exact_observations = [
        {
            row.block_id: row
            for row in observe_blocks(
                snapshot.state,
                grid,
                config.preparation_time + snapshot.time,
            )
        }
        for snapshot in exact.snapshots
    ]
    kinetic_observations = [
        {
            row.block_id: row
            for row in observe_blocks(
                snapshot.state,
                grid,
                config.preparation_time + snapshot.time,
            )
        }
        for snapshot in kinetic.snapshots
    ]
    exact_collision_history = (
        tuple(preparation.collision_events)
        + _shift_collision_events(exact.collision_events, config.preparation_time)
    )
    exact_geometry_history = (
        tuple(preparation.geometry_collision_events)
        + _shift_geometry_events(exact.geometry_collision_events, config.preparation_time)
    )
    future_steps = round(config.future_horizon / config.sample_interval)
    global_density = particle_count / observation_domain.area
    velocity_scale = sqrt(max(case.temperature, 1.0e-12) / case.particle_mass)
    rows: list[DiscrepancyRow] = []

    for sample_index in range(0, len(exact.snapshots) - future_steps):
        time_since_release = exact.snapshots[sample_index].time
        time = config.preparation_time + exact.snapshots[sample_index].time
        future_index = sample_index + future_steps
        future_time = config.preparation_time + exact.snapshots[future_index].time
        for iy in range(grid.cells_y):
            for ix in range(grid.cells_x):
                block_id = f"b-{ix:02d}-{iy:02d}"
                exact_now = exact_observations[sample_index][block_id]
                kinetic_now = kinetic_observations[sample_index][block_id]
                exact_future = exact_observations[future_index][block_id]
                kinetic_future = kinetic_observations[future_index][block_id]
                if min(exact_now.sample_count, kinetic_now.sample_count) < (
                    config.minimum_block_samples
                ):
                    continue
                state_features = kinetic_now.state_features()
                geometry_features = grid.geometry_features(ix, iy)
                exact_state = exact.snapshots[sample_index].state
                current_exact_particle_ids = {
                    exact_state.particle_ids[index]
                    for index, position in enumerate(exact_state.positions)
                    if grid.index(position) == (ix, iy)
                }
                history_features = summarize_history_window(
                    exact_collision_history,
                    block_id=block_id,
                    window_start=max(0.0, time - config.history_window),
                    window_end=time,
                    geometry_events=exact_geometry_history,
                    particle_ids=current_exact_particle_ids,
                )
                targets = _future_targets(
                    exact_future.target_observables(),
                    kinetic_future.target_observables(),
                    global_density=global_density,
                    temperature_scale=case.temperature,
                    velocity_scale=velocity_scale,
                )
                numerical_features = {
                    "dsmc_cell_width_over_diameter": observation_domain.width
                    / config.dsmc_cells_x
                    / (2.0 * case.particle_radius),
                    "dsmc_cell_height_over_diameter": observation_domain.height
                    / config.dsmc_cells_y
                    / (2.0 * case.particle_radius),
                    "dsmc_time_step": config.dsmc_time_step,
                    "particle_weight": 1.0,
                    "time_since_release": time_since_release,
                    "global_number_density": global_density,
                    "temperature_scale": case.temperature,
                    "velocity_scale": velocity_scale,
                }
                visibility = {
                    **{name: "runtime_observable" for name in state_features},
                    **{name: "runtime_observable" for name in geometry_features},
                    **{name: "runtime_observable" for name in numerical_features},
                    **{name: "oracle_only" for name in history_features},
                }
                rows.append(
                    DiscrepancyRow(
                        schema_version="1.0.0",
                        study_id=config.study_id,
                        case_id=case.case_id,
                        geometry_id=case.geometry_id,
                        state_id=case.state_id,
                        seed=seed,
                        trajectory_group=f"{case.case_id}/seed-{seed}",
                        block_id=block_id,
                        time=time,
                        future_time=future_time,
                        state_features=state_features,
                        geometry_features=geometry_features,
                        numerical_features=numerical_features,
                        history_features=history_features,
                        feature_visibility=visibility,
                        targets=targets,
                        paired_observables={
                            "exact_current": exact_now.target_observables(),
                            "kinetic_current": kinetic_now.target_observables(),
                            "exact_future": exact_future.target_observables(),
                            "kinetic_future": kinetic_future.target_observables(),
                        },
                        ensemble_members=(seed,),
                    )
                )

    audit = PairedRunAudit(
        case_id=case.case_id,
        seed=seed,
        particle_count=particle_count,
        exact_collision_count=len(exact_collision_history),
        kinetic_collision_count=len(kinetic.collision_events),
        exact_relative_energy_error=exact.diagnostics.relative_energy_error,
        kinetic_relative_energy_error=kinetic.diagnostics.relative_energy_error,
        exact_absolute_momentum_error=exact.diagnostics.absolute_momentum_error,
        kinetic_absolute_momentum_error=kinetic.diagnostics.absolute_momentum_error,
        row_count=len(rows),
    )
    return rows, audit


def _shift_collision_events(
    events: tuple[CollisionEvent, ...],
    offset: float,
) -> tuple[CollisionEvent, ...]:
    return tuple(
        CollisionEvent(
            time=event.time + offset,
            particle_a=event.particle_a,
            particle_b=event.particle_b,
            block_id=event.block_id,
            pre_velocity_a=event.pre_velocity_a,
            pre_velocity_b=event.pre_velocity_b,
            post_velocity_a=event.post_velocity_a,
            post_velocity_b=event.post_velocity_b,
        )
        for event in events
    )


def _shift_geometry_events(
    events: tuple[GeometryCollisionEvent, ...],
    offset: float,
) -> tuple[GeometryCollisionEvent, ...]:
    return tuple(
        GeometryCollisionEvent(
            time=event.time + offset,
            particle_id=event.particle_id,
            block_id=event.block_id,
            surface_id=event.surface_id,
            pre_velocity=event.pre_velocity,
            post_velocity=event.post_velocity,
        )
        for event in events
    )


def _aggregate_seed_ensembles(
    rows: list[DiscrepancyRow],
    config: PairedStudyConfig,
) -> list[DiscrepancyRow]:
    seed_group = {
        seed: index // config.ensemble_group_size
        for index, seed in enumerate(config.seeds)
    }
    grouped: dict[tuple[str, str, float, int], list[DiscrepancyRow]] = {}
    for row in rows:
        key = (row.case_id, row.block_id, row.time, seed_group[row.seed])
        grouped.setdefault(key, []).append(row)

    aggregated: list[DiscrepancyRow] = []
    for (_, _, _, ensemble_index), members in sorted(grouped.items()):
        if len(members) != config.ensemble_group_size:
            continue
        first = members[0]
        exact_current = _mean_mapping(
            [member.paired_observables["exact_current"] for member in members]
        )
        kinetic_current = _mean_mapping(
            [member.paired_observables["kinetic_current"] for member in members]
        )
        exact_future = _mean_mapping(
            [member.paired_observables["exact_future"] for member in members]
        )
        kinetic_future = _mean_mapping(
            [member.paired_observables["kinetic_future"] for member in members]
        )
        numerical = first.numerical_features
        state_features = _mean_mapping([member.state_features for member in members])
        targets = _future_targets(
            exact_future,
            kinetic_future,
            global_density=numerical["global_number_density"],
            temperature_scale=numerical["temperature_scale"],
            velocity_scale=numerical["velocity_scale"],
        )
        seeds = tuple(sorted(member.seed for member in members))
        aggregated.append(
            DiscrepancyRow(
                schema_version=first.schema_version,
                study_id=first.study_id,
                case_id=first.case_id,
                geometry_id=first.geometry_id,
                state_id=first.state_id,
                seed=seeds[0],
                trajectory_group=f"{first.case_id}/ensemble-{ensemble_index}",
                block_id=first.block_id,
                time=first.time,
                future_time=first.future_time,
                state_features=state_features,
                geometry_features=first.geometry_features,
                numerical_features=first.numerical_features,
                history_features=_mean_mapping(
                    [member.history_features for member in members]
                ),
                feature_visibility=first.feature_visibility,
                targets=targets,
                paired_observables={
                    "exact_current": exact_current,
                    "kinetic_current": kinetic_current,
                    "exact_future": exact_future,
                    "kinetic_future": kinetic_future,
                    "current_pair_discrepancy": _current_pair_features(
                        exact_current,
                        kinetic_current,
                        global_density=numerical["global_number_density"],
                        temperature_scale=numerical["temperature_scale"],
                        velocity_scale=numerical["velocity_scale"],
                    ),
                },
                ensemble_members=seeds,
            )
        )
    return aggregated


def _mean_mapping(rows: list[dict[str, float]]) -> dict[str, float]:
    if not rows:
        raise ValueError("cannot average an empty mapping sequence")
    keys = set(rows[0])
    if any(set(row) != keys for row in rows):
        raise ValueError("ensemble rows have inconsistent fields")
    return {
        key: sum(row[key] for row in rows) / len(rows)
        for key in sorted(keys)
    }


def _current_pair_features(
    exact: dict[str, float],
    kinetic: dict[str, float],
    *,
    global_density: float,
    temperature_scale: float,
    velocity_scale: float,
) -> dict[str, float]:
    return {
        "current_density_discrepancy": abs(
            exact["number_density"] - kinetic["number_density"]
        )
        / max(global_density, 1.0e-30),
        "current_temperature_discrepancy": abs(
            exact["temperature"] - kinetic["temperature"]
        )
        / max(temperature_scale, 1.0e-30),
        "current_velocity_discrepancy": hypot(
            exact["mean_velocity_x"] - kinetic["mean_velocity_x"],
            exact["mean_velocity_y"] - kinetic["mean_velocity_y"],
        )
        / max(velocity_scale, 1.0e-30),
    }


def _future_targets(
    exact: dict[str, float],
    kinetic: dict[str, float],
    *,
    global_density: float,
    temperature_scale: float,
    velocity_scale: float,
) -> dict[str, float]:
    density_error = abs(exact["number_density"] - kinetic["number_density"]) / max(
        global_density, 1.0e-30
    )
    temperature_error = abs(exact["temperature"] - kinetic["temperature"]) / max(
        temperature_scale, 1.0e-30
    )
    velocity_error = hypot(
        exact["mean_velocity_x"] - kinetic["mean_velocity_x"],
        exact["mean_velocity_y"] - kinetic["mean_velocity_y"],
    ) / max(velocity_scale, 1.0e-30)
    distribution_error = abs(
        exact["maxwellian_residual"] - kinetic["maxwellian_residual"]
    )
    composite = sqrt(
        (
            density_error * density_error
            + temperature_error * temperature_error
            + velocity_error * velocity_error
            + distribution_error * distribution_error
        )
        / 4.0
    )
    return {
        "future_density_error": density_error,
        "future_temperature_error": temperature_error,
        "future_velocity_error": velocity_error,
        "future_distribution_error": distribution_error,
        "future_composite_error": composite,
    }


def write_study(result: PairedStudyResult, output_directory: Path) -> tuple[Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    dataset_path = output_directory / "discrepancy-dataset.jsonl"
    dataset_text = "".join(
        json.dumps(asdict(row), sort_keys=True, separators=(",", ":")) + "\n"
        for row in result.rows
    )
    dataset_path.write_text(dataset_text, encoding="utf-8")
    dataset_sha256 = hashlib.sha256(dataset_text.encode("utf-8")).hexdigest()
    config_payload = _config_identity_payload(result.config)
    manifest = {
        "schema_version": "1.0.0",
        "study_id": result.config.study_id,
        "study_content_id": content_id("paired-study", config_payload),
        "config": config_payload,
        "dataset": {
            "path": dataset_path.name,
            "sha256": dataset_sha256,
            "row_count": len(result.rows),
        },
        "groups": {
            "geometry_ids": sorted({row.geometry_id for row in result.rows}),
            "state_ids": sorted({row.state_id for row in result.rows}),
            "trajectory_groups": len({row.trajectory_group for row in result.rows}),
        },
        "audits": [asdict(audit) for audit in result.audits],
    }
    manifest_path = output_directory / "study-manifest.json"
    manifest_path.write_text(canonical_json(manifest) + "\n", encoding="utf-8")
    return dataset_path, manifest_path


def _config_identity_payload(config: PairedStudyConfig) -> dict[str, Any]:
    return {
        "study_id": config.study_id,
        "cases": [
            {
                **asdict(case),
                "domain": {
                    "lower": case.domain.lower,
                    "upper": case.domain.upper,
                    "boundary": case.domain.boundary.value,
                    "obstacles": [asdict(obstacle) for obstacle in case.domain.obstacles],
                },
            }
            for case in config.cases
        ],
        "seeds": config.seeds,
        "preparation_time": config.preparation_time,
        "end_time": config.end_time,
        "sample_interval": config.sample_interval,
        "future_horizon": config.future_horizon,
        "history_window": config.history_window,
        "blocks_x": config.blocks_x,
        "blocks_y": config.blocks_y,
        "dsmc_cells_x": config.dsmc_cells_x,
        "dsmc_cells_y": config.dsmc_cells_y,
        "dsmc_time_step": config.dsmc_time_step,
        "minimum_block_samples": config.minimum_block_samples,
        "ensemble_group_size": config.ensemble_group_size,
    }


def _kinetic_seed(case_id: str, seed: int) -> int:
    digest = hashlib.sha256(f"{case_id}:{seed}:dsmc".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def _domain_from_mapping(payload: dict[str, Any]) -> Domain2D:
    obstacles = tuple(
        CircleObstacle(
            obstacle_id=str(raw["obstacle_id"]),
            center=_float_pair(raw["center"], "obstacle center"),
            radius=float(raw["radius"]),
        )
        for raw in _sequence_of_mappings(payload.get("obstacles", []), "obstacles")
    )
    return Domain2D(
        lower=_float_pair(payload["lower"], "domain lower"),
        upper=_float_pair(payload["upper"], "domain upper"),
        boundary=BoundaryKind(str(payload["boundary"])),
        obstacles=obstacles,
    )


def _mapping(value: object, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _sequence_of_mappings(value: object, name: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError(f"{name} must be an array of objects")
    return value


def _float_pair(value: object, name: str) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{name} must contain two numbers")
    return (float(value[0]), float(value[1]))
