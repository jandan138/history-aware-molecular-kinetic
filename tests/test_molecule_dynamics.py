from __future__ import annotations

import pytest

from historykinetic.molecules import (
    EncounterContext,
    EncounterDecision,
    FullCollisionPolicy,
    GhostCollisionPolicy,
    MoleculeTracker,
    PolicyDecision,
)
from historykinetic.solvers import (
    BoundaryKind,
    DiskState,
    Domain2D,
    HardDiskEDMD,
    ModifiedHardDiskEDMD,
    make_initial_state,
)


def test_molecule_tracker_applies_size_and_cycle_rank_budgets() -> None:
    tracker = MoleculeTracker((0, 1, 2, 3))

    assert tracker.budget_allows(0, 1, size=2, cycles=0)[0]
    assert tracker.accept_collision(0, 1, event_id=0).size == 2
    assert not tracker.budget_allows(1, 2, size=2, cycles=0)[0]
    assert tracker.budget_allows(1, 2, size=3, cycles=0)[0]
    assert tracker.accept_collision(1, 2, event_id=1).size == 3
    assert tracker.budget_allows(2, 0, size=3, cycles=1)[0]
    component = tracker.accept_collision(2, 0, event_id=2)
    assert component.cycle_rank == 1
    allowed, reason = tracker.budget_allows(0, 2, size=3, cycles=1)
    assert not allowed
    assert reason == "cycle-rank-budget"
    assert tracker.predecessors(0, 2) == (2, 2)


def test_topology_shuffle_preserves_only_component_budget_signature() -> None:
    tracker = MoleculeTracker(tuple(range(8)))
    tracker.accept_collision(0, 1, event_id=0)
    tracker.accept_collision(1, 2, event_id=1)
    tracker.accept_collision(3, 4, event_id=2)
    tracker.accept_collision(3, 4, event_id=3)
    signature = tracker.component_signature()
    old_membership = tuple(tracker.component(index).component_id for index in range(8))

    tracker.shuffle_membership(seed=19)

    assert tracker.component_signature() == signature
    assert tuple(tracker.component(index).component_id for index in range(8)) != old_membership


def test_full_modified_dynamics_matches_periodic_edmd_event_by_event() -> None:
    domain = Domain2D((0.0, 0.0), (2.0, 1.0), BoundaryKind.PERIODIC)
    state = make_initial_state(
        domain,
        particle_count=18,
        radius=0.025,
        mass=1.0,
        temperature=0.7,
        seed=8,
    )

    reference = HardDiskEDMD(domain).run(state, end_time=0.6, sample_interval=0.1)
    modified = ModifiedHardDiskEDMD(
        domain,
        FullCollisionPolicy(),
        layer_width=0.1,
    ).run(state, end_time=0.6, sample_interval=0.1)

    assert len(modified.encounter_events) == len(reference.collision_events)
    assert modified.overlap_exit_events == ()
    for expected, actual in zip(
        reference.collision_events,
        modified.simulation.collision_events,
        strict=True,
    ):
        assert actual.time == pytest.approx(expected.time, abs=1.0e-12)
        assert actual.ordered_pair == expected.ordered_pair
        assert actual.post_velocity_a == pytest.approx(expected.post_velocity_a)
        assert actual.post_velocity_b == pytest.approx(expected.post_velocity_b)
    for expected, actual in zip(
        reference.snapshots,
        modified.simulation.snapshots,
        strict=True,
    ):
        assert actual.state.positions == pytest.approx(expected.state.positions)
        assert actual.state.velocities == pytest.approx(expected.state.velocities)


def test_ghost_policy_logs_entry_and_exit_without_impulse() -> None:
    domain = Domain2D((0.0, 0.0), (4.0, 1.0), BoundaryKind.PERIODIC)
    state = DiskState(
        positions=[(1.0, 0.5), (2.0, 0.5)],
        velocities=[(1.0, 0.0), (0.0, 0.0)],
        radii=[0.1, 0.1],
        masses=[1.0, 1.0],
        particle_ids=[0, 1],
        weights=[1.0, 1.0],
    )

    result = ModifiedHardDiskEDMD(
        domain,
        GhostCollisionPolicy(),
        layer_width=0.1,
    ).run(state, end_time=1.4, sample_interval=0.2)

    assert len(result.encounter_events) == 1
    assert result.encounter_events[0].time == pytest.approx(0.8)
    assert result.encounter_events[0].decision is EncounterDecision.SUPPRESS
    assert result.encounter_events[0].pre_velocity_a == (1.0, 0.0)
    assert result.encounter_events[0].post_velocity_a == (1.0, 0.0)
    assert len(result.overlap_exit_events) == 1
    assert result.overlap_exit_events[0].time == pytest.approx(1.2)
    assert result.simulation.collision_events == ()
    assert result.simulation.snapshots[-1].state.positions == pytest.approx(
        [(2.4, 0.5), (2.0, 0.5)]
    )
    assert result.maximum_simultaneous_overlaps == 1


def test_third_particle_impulse_invalidates_active_overlap_exit() -> None:
    class SuppressOnlyFirstPair:
        name = "suppress-0-1"

        def decide(
            self,
            context: EncounterContext,
            tracker: MoleculeTracker,
        ) -> PolicyDecision:
            del tracker
            pair = tuple(sorted((context.particle_a, context.particle_b)))
            if pair == (0, 1):
                return PolicyDecision(EncounterDecision.SUPPRESS, "selected-pair")
            return PolicyDecision(EncounterDecision.ACCEPT, "other-pair")

    domain = Domain2D((0.0, 0.0), (5.0, 2.0), BoundaryKind.PERIODIC)
    state = DiskState(
        positions=[(1.0, 0.5), (2.0, 0.5), (1.9, 0.05)],
        velocities=[(1.0, 0.0), (0.0, 0.0), (0.0, 0.25 / 0.9)],
        radii=[0.1, 0.1, 0.1],
        masses=[1.0, 1.0, 1.0],
        particle_ids=[0, 1, 2],
        weights=[1.0, 1.0, 1.0],
    )

    result = ModifiedHardDiskEDMD(
        domain,
        SuppressOnlyFirstPair(),
        layer_width=0.1,
    ).run(state, end_time=1.3, sample_interval=0.1)

    suppressed = result.suppressed_encounters
    assert len(suppressed) == 1
    assert suppressed[0].ordered_pair == (0, 1)
    assert any(event.ordered_pair == (0, 2) for event in result.accepted_encounters)
    overlap_exit = next(
        event
        for event in result.overlap_exit_events
        if tuple(sorted((event.particle_a, event.particle_b))) == (0, 1)
    )
    assert overlap_exit.time != pytest.approx(1.2, abs=1.0e-6)
    assert 0.9 < overlap_exit.time < 1.3
