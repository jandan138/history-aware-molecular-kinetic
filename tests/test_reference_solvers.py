from __future__ import annotations

import statistics

import pytest

from historykinetic.solvers import (
    BoundaryKind,
    DiskState,
    Domain2D,
    HardDiskDSMC,
    HardDiskEDMD,
    make_initial_state,
)


def test_edmd_two_disk_collision_matches_analytic_time_and_response() -> None:
    domain = Domain2D((0.0, 0.0), (1.0, 1.0), BoundaryKind.REFLECTIVE)
    state = DiskState(
        positions=[(0.25, 0.5), (0.75, 0.5)],
        velocities=[(1.0, 0.0), (-1.0, 0.0)],
        radii=[0.05, 0.05],
        masses=[1.0, 1.0],
        particle_ids=[0, 1],
        weights=[1.0, 1.0],
    )

    result = HardDiskEDMD(domain).run(state, end_time=0.3, sample_interval=0.1)

    assert len(result.collision_events) == 1
    assert result.collision_events[0].time == pytest.approx(0.2, abs=1.0e-12)
    assert result.collision_events[0].post_velocity_a[:2] == pytest.approx((-1.0, 0.0))
    assert result.collision_events[0].post_velocity_b[:2] == pytest.approx((1.0, 0.0))
    assert result.collision_events[0].contact_normal == pytest.approx((1.0, 0.0))
    assert result.collision_events[0].incoming_relative_normal_velocity == pytest.approx(
        2.0
    )
    assert result.diagnostics.relative_energy_error <= 1.0e-14


def test_exact_and_kinetic_references_share_samples_and_conserve_energy() -> None:
    domain = Domain2D((0.0, 0.0), (1.0, 1.0), BoundaryKind.PERIODIC)
    state = make_initial_state(
        domain,
        particle_count=24,
        radius=0.025,
        mass=1.0,
        temperature=1.0,
        seed=7,
    )
    exact = HardDiskEDMD(domain).run(state, end_time=0.2, sample_interval=0.05)
    kinetic = HardDiskDSMC(
        domain,
        cells_x=3,
        cells_y=3,
        time_step=0.005,
        seed=8,
    ).run(state, end_time=0.2, sample_interval=0.05)

    assert [snapshot.time for snapshot in exact.snapshots] == pytest.approx(
        [snapshot.time for snapshot in kinetic.snapshots]
    )
    assert exact.event_semantics == "geometric_collision"
    assert kinetic.event_semantics == "kinetic_collision"
    assert exact.diagnostics.relative_energy_error <= 1.0e-13
    assert kinetic.diagnostics.relative_energy_error <= 1.0e-13
    assert exact.diagnostics.absolute_momentum_error <= 1.0e-13
    assert kinetic.diagnostics.absolute_momentum_error <= 1.0e-13


def test_dilute_exact_and_kinetic_collision_rates_agree() -> None:
    domain = Domain2D((0.0, 0.0), (2.0, 1.0), BoundaryKind.PERIODIC)
    exact_rates: list[float] = []
    kinetic_rates: list[float] = []
    for seed in range(6):
        state = make_initial_state(
            domain,
            particle_count=48,
            radius=0.02,
            mass=1.0,
            temperature=1.0,
            seed=seed,
        )
        exact = HardDiskEDMD(domain).run(state, end_time=1.0, sample_interval=1.0)
        kinetic = HardDiskDSMC(
            domain,
            cells_x=8,
            cells_y=4,
            time_step=0.005,
            seed=1000 + seed,
        ).run(state, end_time=1.0, sample_interval=1.0)
        exact_rates.append(float(len(exact.collision_events)))
        kinetic_rates.append(float(len(kinetic.collision_events)))

    exact_mean = statistics.mean(exact_rates)
    kinetic_mean = statistics.mean(kinetic_rates)
    assert abs(exact_mean - kinetic_mean) / exact_mean <= 0.15
