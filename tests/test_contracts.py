from pathlib import PurePosixPath

import pytest

from historykinetic.contracts import ArtifactRef, CollisionEvent, ConservationBudget


def event(a: int = 1, b: int = 2) -> CollisionEvent:
    zero = (0.0, 0.0, 0.0)
    return CollisionEvent(0.0, a, b, "b0", zero, zero, zero, zero)


def test_collision_pair_is_canonical() -> None:
    assert event(9, 2).ordered_pair == (2, 9)


def test_self_collision_rejected() -> None:
    with pytest.raises(ValueError):
        event(3, 3)


def test_artifact_path_must_be_relative() -> None:
    with pytest.raises(ValueError):
        ArtifactRef("particles", PurePosixPath("/absolute"), "1.0.0")


def test_conservation_budget() -> None:
    budget = ConservationBudget(2.0, 2.1, (0.0, 0.0, 0.0), (0.1, 0.0, 0.0), 4.0, 4.0)
    assert budget.relative_mass_error == pytest.approx(0.05)
    assert budget.relative_energy_error == 0.0
    assert budget.absolute_momentum_error == pytest.approx(0.1)
