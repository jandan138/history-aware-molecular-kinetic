"""Grouped/OOD evaluation for state-only versus state+history prediction."""

from __future__ import annotations

import json
import random
from collections import defaultdict
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

STATE_NAMESPACES = ("state_features", "geometry_features", "numerical_features")
HISTORY_NAMESPACE = "history_features"
DEFAULT_TARGET_NAME = "future_composite_error"


@dataclass(frozen=True, slots=True)
class FoldResult:
    split_axis: str
    held_out_group: str
    train_trajectory_count: int
    test_trajectory_count: int
    test_row_count: int
    state_mae: float
    history_mae: float
    relative_mae_improvement: float
    state_rmse: float
    history_rmse: float
    high_error_budget: float
    state_high_error_coverage: float
    history_high_error_coverage: float
    state_residual_error_fraction: float
    history_residual_error_fraction: float


def load_dataset(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not rows:
        raise ValueError("discrepancy dataset is empty")
    return rows


def evaluate_grouped(
    rows: list[dict[str, Any]],
    *,
    model_kind: str = "hist_gradient_boosting",
    target_name: str = DEFAULT_TARGET_NAME,
    maximum_time_since_release: float | None = None,
    high_error_budget: float = 0.2,
    bootstrap_repetitions: int = 500,
    seed: int = 1729,
) -> dict[str, Any]:
    if maximum_time_since_release is not None:
        rows = [
            row
            for row in rows
            if float(row["numerical_features"]["time_since_release"])
            <= maximum_time_since_release + 1.0e-12
        ]
        if not rows:
            raise ValueError("time-since-release filter removed every row")
    np, models = _analysis_dependencies()
    state_names = _feature_names(rows, STATE_NAMESPACES)
    history_names = state_names + _feature_names(rows, (HISTORY_NAMESPACE,))
    folds: list[FoldResult] = []
    prediction_rows: list[dict[str, Any]] = []

    split_definitions: tuple[
        tuple[str, Callable[[dict[str, Any]], str]], ...
    ] = (
        ("geometry_id", lambda row: str(row["geometry_id"])),
        ("state_id", lambda row: str(row["state_id"])),
        (
            "ensemble_group",
            lambda row: ",".join(str(seed) for seed in row["ensemble_members"]),
        ),
    )
    for split_axis, group_value in split_definitions:
        held_out_groups = sorted({group_value(row) for row in rows})
        if len(held_out_groups) < 2:
            continue
        for held_out in held_out_groups:
            train = [row for row in rows if group_value(row) != held_out]
            test = [row for row in rows if group_value(row) == held_out]
            train_groups = {str(row["trajectory_group"]) for row in train}
            test_groups = {str(row["trajectory_group"]) for row in test}
            if train_groups & test_groups:
                raise RuntimeError("trajectory leakage across grouped split")
            if not train or not test:
                raise RuntimeError(f"empty grouped fold for {split_axis}={held_out}")

            if any(target_name not in row["targets"] for row in (*train, *test)):
                raise ValueError(f"unknown discrepancy target: {target_name}")
            y_train = np.asarray([float(row["targets"][target_name]) for row in train])
            y_test = np.asarray([float(row["targets"][target_name]) for row in test])
            state_model = _make_model(model_kind, seed, models)
            history_model = _make_model(model_kind, seed, models)
            state_model.fit(_matrix(np, train, state_names), y_train)
            history_model.fit(_matrix(np, train, history_names), y_train)
            state_prediction = np.maximum(
                0.0, state_model.predict(_matrix(np, test, state_names))
            )
            history_prediction = np.maximum(
                0.0, history_model.predict(_matrix(np, test, history_names))
            )
            state_mae = float(np.mean(np.abs(state_prediction - y_test)))
            history_mae = float(np.mean(np.abs(history_prediction - y_test)))
            state_rmse = float(np.sqrt(np.mean((state_prediction - y_test) ** 2)))
            history_rmse = float(np.sqrt(np.mean((history_prediction - y_test) ** 2)))
            folds.append(
                FoldResult(
                    split_axis=split_axis,
                    held_out_group=held_out,
                    train_trajectory_count=len(train_groups),
                    test_trajectory_count=len(test_groups),
                    test_row_count=len(test),
                    state_mae=state_mae,
                    history_mae=history_mae,
                    relative_mae_improvement=(state_mae - history_mae)
                    / max(state_mae, 1.0e-30),
                    state_rmse=state_rmse,
                    history_rmse=history_rmse,
                    high_error_budget=high_error_budget,
                    state_high_error_coverage=_top_budget_coverage(
                        np, y_test, state_prediction, high_error_budget
                    ),
                    history_high_error_coverage=_top_budget_coverage(
                        np, y_test, history_prediction, high_error_budget
                    ),
                    state_residual_error_fraction=_oracle_residual_fraction(
                        np, y_test, state_prediction, high_error_budget
                    ),
                    history_residual_error_fraction=_oracle_residual_fraction(
                        np, y_test, history_prediction, high_error_budget
                    ),
                )
            )
            for row, target, state_value, history_value in zip(
                test, y_test, state_prediction, history_prediction, strict=True
            ):
                prediction_rows.append(
                    {
                        "split_axis": split_axis,
                        "held_out_group": held_out,
                        "trajectory_group": row["trajectory_group"],
                        "case_id": row["case_id"],
                        "seed": row["seed"],
                        "block_id": row["block_id"],
                        "time": row["time"],
                        "target": float(target),
                        "state_prediction": float(state_value),
                        "history_prediction": float(history_value),
                    }
                )

    ood_prediction_rows = [
        row for row in prediction_rows if row["split_axis"] != "ensemble_group"
    ]
    ensemble_prediction_rows = [
        row for row in prediction_rows if row["split_axis"] == "ensemble_group"
    ]
    bootstrap = _grouped_bootstrap(
        ood_prediction_rows,
        repetitions=bootstrap_repetitions,
        seed=seed,
    )
    ensemble_bootstrap = _grouped_bootstrap(
        ensemble_prediction_rows,
        repetitions=bootstrap_repetitions,
        seed=seed + 1,
    )
    ood_folds = [fold for fold in folds if fold.split_axis != "ensemble_group"]
    return {
        "schema_version": "1.0.0",
        "target": target_name,
        "maximum_time_since_release": maximum_time_since_release,
        "model_kind": model_kind,
        "state_feature_names": state_names,
        "history_feature_names": [
            name for name in history_names if name not in state_names
        ],
        "observability": {
            "state_model_uses_oracle_only": False,
            "history_model_role": "oracle_upper_bound",
        },
        "folds": [asdict(fold) for fold in folds],
        "aggregate": {
            "mean_relative_mae_improvement": sum(
                fold.relative_mae_improvement for fold in ood_folds
            )
            / len(ood_folds),
            "geometry_mean_relative_mae_improvement": _fold_mean(
                folds, "geometry_id", "relative_mae_improvement"
            ),
            "state_mean_relative_mae_improvement": _fold_mean(
                folds, "state_id", "relative_mae_improvement"
            ),
            "ensemble_mean_relative_mae_improvement": _fold_mean(
                folds, "ensemble_group", "relative_mae_improvement"
            ),
            "mean_state_high_error_coverage": sum(
                fold.state_high_error_coverage for fold in ood_folds
            )
            / len(ood_folds),
            "mean_history_high_error_coverage": sum(
                fold.history_high_error_coverage for fold in ood_folds
            )
            / len(ood_folds),
            "mean_state_residual_error_fraction": sum(
                fold.state_residual_error_fraction for fold in ood_folds
            )
            / len(ood_folds),
            "mean_history_residual_error_fraction": sum(
                fold.history_residual_error_fraction for fold in ood_folds
            )
            / len(ood_folds),
            "grouped_bootstrap": bootstrap,
            "ensemble_grouped_bootstrap": ensemble_bootstrap,
        },
        "predictions": prediction_rows,
    }


def write_evaluation(report: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def _analysis_dependencies() -> tuple[Any, dict[str, Any]]:
    try:
        import numpy as np  # type: ignore[import-not-found]
        from sklearn.ensemble import (  # type: ignore[import-not-found]
            HistGradientBoostingRegressor,
        )
        from sklearn.linear_model import Ridge  # type: ignore[import-not-found]
        from sklearn.pipeline import make_pipeline  # type: ignore[import-not-found]
        from sklearn.preprocessing import StandardScaler  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            'analysis dependencies are required; install with pip install -e ".[analysis]"'
        ) from exc
    return (
        np,
        {
            "HistGradientBoostingRegressor": HistGradientBoostingRegressor,
            "Ridge": Ridge,
            "make_pipeline": make_pipeline,
            "StandardScaler": StandardScaler,
        },
    )


def _make_model(kind: str, seed: int, models: dict[str, Any]) -> Any:
    if kind == "hist_gradient_boosting":
        return models["HistGradientBoostingRegressor"](
            max_iter=180,
            learning_rate=0.05,
            max_leaf_nodes=15,
            min_samples_leaf=20,
            l2_regularization=1.0,
            random_state=seed,
        )
    if kind == "ridge":
        return models["make_pipeline"](
            models["StandardScaler"](),
            models["Ridge"](alpha=10.0),
        )
    raise ValueError(f"unknown model kind: {kind}")


def _feature_names(
    rows: list[dict[str, Any]], namespaces: tuple[str, ...]
) -> list[str]:
    names: list[str] = []
    for namespace in namespaces:
        keys = sorted(
            {
                str(key)
                for row in rows
                for key in _feature_mapping(row, namespace)
            }
        )
        names.extend(f"{namespace}.{key}" for key in keys)
    return names


def _matrix(np: Any, rows: list[dict[str, Any]], names: list[str]) -> Any:
    return np.asarray(
        [
            [
                float(_feature_mapping(row, namespace)[key])
                for namespace, key in (name.split(".", 1) for name in names)
            ]
            for row in rows
        ],
        dtype=float,
    )


def _feature_mapping(row: dict[str, Any], namespace: str) -> dict[str, Any]:
    value = row[namespace]
    if not isinstance(value, dict):
        raise ValueError(f"{namespace} must be an object")
    return value


def _top_budget_coverage(
    np: Any,
    targets: Any,
    predictions: Any,
    budget: float,
) -> float:
    if not 0 < budget < 1:
        raise ValueError("high-error budget must lie in (0, 1)")
    count = max(1, round(len(targets) * budget))
    actual_high = set(np.argsort(targets)[-count:].tolist())
    predicted_high = set(np.argsort(predictions)[-count:].tolist())
    return len(actual_high & predicted_high) / count


def _oracle_residual_fraction(
    np: Any,
    targets: Any,
    predictions: Any,
    budget: float,
) -> float:
    count = max(1, round(len(targets) * budget))
    selected = set(np.argsort(predictions)[-count:].tolist())
    residual = sum(float(value) for index, value in enumerate(targets) if index not in selected)
    return residual / max(float(np.sum(targets)), 1.0e-30)


def _grouped_bootstrap(
    predictions: list[dict[str, Any]],
    *,
    repetitions: int,
    seed: int,
) -> dict[str, float]:
    rng = random.Random(seed)
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in predictions:
        key = f"{row['split_axis']}:{row['held_out_group']}:{row['trajectory_group']}"
        by_group[key].append(row)
    groups = sorted(by_group)
    improvements: list[float] = []
    for _ in range(repetitions):
        sample = [rng.choice(groups) for _ in groups]
        selected = [row for group in sample for row in by_group[group]]
        state_mae = sum(
            abs(float(row["state_prediction"]) - float(row["target"])) for row in selected
        ) / len(selected)
        history_mae = sum(
            abs(float(row["history_prediction"]) - float(row["target"]))
            for row in selected
        ) / len(selected)
        improvements.append((state_mae - history_mae) / max(state_mae, 1.0e-30))
    improvements.sort()
    return {
        "repetitions": float(repetitions),
        "mean_relative_mae_improvement": sum(improvements) / len(improvements),
        "ci95_low": _quantile(improvements, 0.025),
        "ci95_high": _quantile(improvements, 0.975),
    }


def _quantile(sorted_values: list[float], probability: float) -> float:
    position = probability * (len(sorted_values) - 1)
    lower = int(position)
    upper = min(len(sorted_values) - 1, lower + 1)
    fraction = position - lower
    return sorted_values[lower] * (1.0 - fraction) + sorted_values[upper] * fraction


def _fold_mean(folds: list[FoldResult], axis: str, field: str) -> float:
    selected = [fold for fold in folds if fold.split_axis == axis]
    if not selected:
        return float("nan")
    return sum(float(getattr(fold, field)) for fold in selected) / len(selected)
