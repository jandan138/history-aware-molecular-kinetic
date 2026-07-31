"""Find figure-ready pairs with matched present state and different history."""

from __future__ import annotations

import json
from collections import defaultdict
from math import sqrt
from pathlib import Path
from typing import Any

from historykinetic.studies.evaluate import load_dataset


def find_matched_state_pairs(
    rows: list[dict[str, Any]],
    *,
    limit: int = 24,
    maximum_state_distance: float = 0.5,
) -> dict[str, Any]:
    state_names = sorted(
        {
            name
            for row in rows
            for name in _float_mapping(row["state_features"], "state_features")
            if name != "sample_count"
        }
    )
    history_names = sorted(
        {
            name
            for row in rows
            for name in _float_mapping(row["history_features"], "history_features")
        }
    )
    state_stats = _feature_stats(rows, "state_features", state_names)
    history_stats = _feature_stats(rows, "history_features", history_names)

    strata: dict[tuple[str, tuple[int, ...], float], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (
            str(row["state_id"]),
            tuple(int(seed) for seed in row["ensemble_members"]),
            float(row["time"]),
        )
        strata[key].append(row)

    candidates: list[dict[str, Any]] = []
    for members in strata.values():
        for left_index, left in enumerate(members):
            for right in members[left_index + 1 :]:
                if left["geometry_id"] == right["geometry_id"]:
                    continue
                state_distance = _distance(
                    left,
                    right,
                    namespace="state_features",
                    names=state_names,
                    stats=state_stats,
                )
                if state_distance > maximum_state_distance:
                    continue
                history_distance = _distance(
                    left,
                    right,
                    namespace="history_features",
                    names=history_names,
                    stats=history_stats,
                )
                target_gap = abs(
                    float(left["targets"]["future_composite_error"])
                    - float(right["targets"]["future_composite_error"])
                )
                score = history_distance * target_gap / (0.25 + state_distance)
                candidates.append(
                    {
                        "score": score,
                        "state_distance": state_distance,
                        "history_distance": history_distance,
                        "future_error_gap": target_gap,
                        "left": _figure_row(left),
                        "right": _figure_row(right),
                    }
                )

    candidates.sort(key=lambda row: float(row["score"]), reverse=True)
    selected: list[dict[str, Any]] = []
    used: set[tuple[str, int, str, float]] = set()
    for candidate in candidates:
        left_key = _row_key(candidate["left"])
        right_key = _row_key(candidate["right"])
        if left_key in used or right_key in used:
            continue
        selected.append(candidate)
        used.update((left_key, right_key))
        if len(selected) >= limit:
            break

    return {
        "schema_version": "1.0.0",
        "selection_role": "descriptive_figure_candidates_not_model_evaluation",
        "matching": {
            "same_state_family": True,
            "same_seed_ensemble": True,
            "same_time": True,
            "different_geometry": True,
            "maximum_standardized_state_distance": maximum_state_distance,
            "state_feature_names": state_names,
            "history_feature_names": history_names,
        },
        "candidate_count": len(candidates),
        "selected_pairs": selected,
    }


def write_matched_pairs(report: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _feature_stats(
    rows: list[dict[str, Any]],
    namespace: str,
    names: list[str],
) -> dict[str, tuple[float, float]]:
    stats: dict[str, tuple[float, float]] = {}
    for name in names:
        values = [
            float(_float_mapping(row[namespace], namespace)[name])
            for row in rows
        ]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        stats[name] = (mean, max(variance**0.5, 1.0e-12))
    return stats


def _distance(
    left: dict[str, Any],
    right: dict[str, Any],
    *,
    namespace: str,
    names: list[str],
    stats: dict[str, tuple[float, float]],
) -> float:
    left_features = _float_mapping(left[namespace], namespace)
    right_features = _float_mapping(right[namespace], namespace)
    return sqrt(
        sum(
            (
                (float(left_features[name]) - float(right_features[name]))
                / stats[name][1]
            )
            ** 2
            for name in names
        )
        / max(len(names), 1)
    )


def _figure_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": row["case_id"],
        "geometry_id": row["geometry_id"],
        "state_id": row["state_id"],
        "ensemble_members": row["ensemble_members"],
        "block_id": row["block_id"],
        "time": row["time"],
        "future_time": row["future_time"],
        "state_features": row["state_features"],
        "geometry_features": row["geometry_features"],
        "history_features": row["history_features"],
        "current_pair_discrepancy": row["paired_observables"][
            "current_pair_discrepancy"
        ],
        "future_exact": row["paired_observables"]["exact_future"],
        "future_kinetic": row["paired_observables"]["kinetic_future"],
        "targets": row["targets"],
    }


def _row_key(row: dict[str, Any]) -> tuple[str, int, str, float]:
    return (
        str(row["case_id"]),
        int(row["ensemble_members"][0]),
        str(row["block_id"]),
        float(row["time"]),
    )


def _float_mapping(value: object, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def matched_pairs_from_dataset(
    dataset: Path,
    output: Path,
    *,
    limit: int = 24,
    maximum_state_distance: float = 0.5,
) -> Path:
    return write_matched_pairs(
        find_matched_state_pairs(
            load_dataset(dataset),
            limit=limit,
            maximum_state_distance=maximum_state_distance,
        ),
        output,
    )
