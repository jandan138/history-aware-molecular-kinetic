from historykinetic.contracts import CollisionEvent
from historykinetic.graphs import RollingCollisionWindow, summarize_collision_graph

ZERO = (0.0, 0.0, 0.0)


def e(t: float, a: int, b: int) -> CollisionEvent:
    return CollisionEvent(t, a, b, "b0", ZERO, ZERO, ZERO, ZERO)


def test_tree_has_zero_cycle_rank() -> None:
    summary = summarize_collision_graph([e(0, 0, 1), e(1, 1, 2), e(2, 2, 3)])
    assert summary.cycle_rank == 0
    assert summary.component_count == 1


def test_triangle_has_one_cycle() -> None:
    summary = summarize_collision_graph([e(0, 0, 1), e(1, 1, 2), e(2, 2, 0)])
    assert summary.cycle_rank == 1


def test_repeated_pair_ratio_counts_extra_events() -> None:
    summary = summarize_collision_graph([e(0, 0, 1), e(1, 0, 1), e(2, 1, 2)])
    assert summary.unique_pair_count == 2
    assert summary.repeated_pair_ratio == 1 / 3


def test_rolling_window_expires_old_events() -> None:
    window = RollingCollisionWindow(2.0)
    window.extend([e(0, 0, 1), e(1, 1, 2), e(3, 2, 3)])
    assert len(window) == 2
    assert window.summary().collision_count == 2
