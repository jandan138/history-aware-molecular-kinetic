from __future__ import annotations

from bisect import bisect_right
from collections import defaultdict
from math import sqrt

from historykinetic.echo.models import (
    EchoMetricRow,
    PassiveColorMap,
    ResolvedStateAudit,
    ReversalAudit,
)
from historykinetic.echo.protocol import EchoBranchKind, EchoE1Protocol
from historykinetic.solvers import DiskState, SimulationResult
from historykinetic.solvers.state import minimum_image


def color_score(
    state: DiskState,
    colors: PassiveColorMap,
    protocol: EchoE1Protocol,
) -> float:
    foreground_total = 0
    foreground_inside = 0
    background_total = 0
    background_outside = 0
    for particle_id, position in zip(state.particle_ids, state.positions, strict=True):
        inside = protocol.pattern.contains(position)
        if colors.label(particle_id) == 1:
            foreground_total += 1
            foreground_inside += int(inside)
        else:
            background_total += 1
            background_outside += int(not inside)
    if foreground_total == 0 or background_total == 0:
        raise ValueError("color score requires both foreground and background particles")
    return 0.5 * (
        foreground_inside / foreground_total + background_outside / background_total
    )


def anisotropy(state: DiskState) -> float:
    total_mass = state.total_mass
    ux, uy = state.momentum
    ux /= total_mass
    uy /= total_mass
    tx = 0.0
    ty = 0.0
    for velocity, mass, weight in zip(
        state.velocities, state.masses, state.weights, strict=True
    ):
        physical_mass = mass * weight
        tx += physical_mass * (velocity[0] - ux) ** 2
        ty += physical_mass * (velocity[1] - uy) ** 2
    denominator = tx + ty
    return (tx - ty) / denominator if denominator > 0 else 0.0


def branch_metrics(
    *,
    particle_count: int,
    seed: int,
    kind: EchoBranchKind,
    result: SimulationResult,
    colors: PassiveColorMap,
    protocol: EchoE1Protocol,
    pivot_score: float,
) -> tuple[EchoMetricRow, ...]:
    denominator = max(1.0 - pivot_score, 1.0e-15)
    return tuple(
        EchoMetricRow(
            particle_count=particle_count,
            seed=seed,
            branch=kind,
            time=snapshot.time,
            color_score=(score := color_score(snapshot.state, colors, protocol)),
            color_recovery=(score - pivot_score) / denominator,
            anisotropy=anisotropy(snapshot.state),
        )
        for snapshot in result.snapshots
    )


def audit_reversal(
    *,
    particle_count: int,
    seed: int,
    initial_state: DiskState,
    forward: SimulationResult,
    reverse: SimulationResult,
    protocol: EchoE1Protocol,
) -> ReversalAudit:
    forward_events = forward.collision_events
    reverse_events = tuple(reversed(reverse.collision_events))
    common = min(len(forward_events), len(reverse_events))
    matching_pairs = sum(
        forward_events[index].ordered_pair == reverse_events[index].ordered_pair
        for index in range(common)
    )
    denominator = max(len(forward_events), len(reverse_events), 1)
    event_pair_agreement = matching_pairs / denominator
    mirrored_errors = [
        abs(
            forward_events[index].time
            + reverse_events[index].time
            - protocol.preparation_time
        )
        for index in range(common)
    ]
    terminal = reverse.snapshots[-1].state
    squared_position_error = 0.0
    squared_velocity_error = 0.0
    for final_position, initial_position, final_velocity, initial_velocity in zip(
        terminal.positions,
        initial_state.positions,
        terminal.velocities,
        initial_state.velocities,
        strict=True,
    ):
        displacement = minimum_image(
            (
                final_position[0] - initial_position[0],
                final_position[1] - initial_position[1],
            ),
            protocol.domain,
        )
        squared_position_error += displacement[0] ** 2 + displacement[1] ** 2
        squared_velocity_error += (
            final_velocity[0] + initial_velocity[0]
        ) ** 2 + (final_velocity[1] + initial_velocity[1]) ** 2
    return ReversalAudit(
        particle_count=particle_count,
        seed=seed,
        forward_event_count=len(forward_events),
        reverse_event_count=len(reverse.collision_events),
        event_pair_agreement=event_pair_agreement,
        maximum_mirrored_event_time_error=max(mirrored_errors, default=0.0),
        position_rms=sqrt(squared_position_error / particle_count),
        velocity_rms=sqrt(squared_velocity_error / particle_count),
        relative_energy_error=reverse.diagnostics.relative_energy_error,
        absolute_momentum_error=reverse.diagnostics.absolute_momentum_error,
    )


def audit_resolved_state(
    *,
    particle_count: int,
    seed: int,
    reference: DiskState,
    candidate: DiskState,
    colors: PassiveColorMap,
    protocol: EchoE1Protocol,
    spatial_grid: tuple[int, int],
    velocity_edges_standardized: tuple[float, ...],
) -> ResolvedStateAudit:
    if reference.particle_ids != candidate.particle_ids:
        raise ValueError("resolved-state audit requires identical particle ordering")
    scale = sqrt(protocol.temperature)
    reference_histogram = _histogram(
        reference,
        colors,
        protocol,
        spatial_grid,
        velocity_edges_standardized,
        scale,
    )
    candidate_histogram = _histogram(
        candidate,
        colors,
        protocol,
        spatial_grid,
        velocity_edges_standardized,
        scale,
    )
    keys = set(reference_histogram) | set(candidate_histogram)
    total_variation = 0.5 * sum(
        abs(reference_histogram.get(key, 0) - candidate_histogram.get(key, 0))
        for key in keys
    ) / particle_count

    reference_moments = _cell_moments(reference, colors, protocol, spatial_grid)
    candidate_moments = _cell_moments(candidate, colors, protocol, spatial_grid)
    moment_keys = set(reference_moments) | set(candidate_moments)
    max_count = 0.0
    max_momentum = 0.0
    max_energy = 0.0
    max_anisotropy = 0.0
    velocity_scale = max(sqrt(protocol.temperature), 1.0e-15)
    energy_scale = max(protocol.temperature, 1.0e-15)
    for key in moment_keys:
        left = reference_moments.get(key, (0, 0.0, 0.0, 0.0, 0.0))
        right = candidate_moments.get(key, (0, 0.0, 0.0, 0.0, 0.0))
        max_count = max(max_count, abs(left[0] - right[0]) / particle_count)
        max_momentum = max(
            max_momentum,
            sqrt((left[1] - right[1]) ** 2 + (left[2] - right[2]) ** 2)
            / (particle_count * velocity_scale),
        )
        max_energy = max(
            max_energy,
            abs(left[3] - right[3]) / (particle_count * energy_scale),
        )
        max_anisotropy = max(
            max_anisotropy,
            abs(left[4] - right[4]) / (particle_count * energy_scale),
        )

    return ResolvedStateAudit(
        particle_count=particle_count,
        seed=seed,
        blocks_x=spatial_grid[0],
        blocks_y=spatial_grid[1],
        velocity_bin_count=len(velocity_edges_standardized) + 1,
        total_variation=total_variation,
        maximum_count_fraction_mismatch=max_count,
        maximum_momentum_mismatch=max_momentum,
        maximum_energy_mismatch=max_energy,
        maximum_anisotropy_mismatch=max_anisotropy,
    )


def invariant_mismatch(reference: DiskState, candidate: DiskState) -> float:
    mass_scale = max(reference.total_mass, 1.0e-30)
    energy_scale = max(reference.kinetic_energy, 1.0e-30)
    momentum_scale = max(sqrt(2.0 * reference.total_mass * reference.kinetic_energy), 1.0e-30)
    momentum_delta = sqrt(
        (reference.momentum[0] - candidate.momentum[0]) ** 2
        + (reference.momentum[1] - candidate.momentum[1]) ** 2
    )
    return max(
        abs(reference.total_mass - candidate.total_mass) / mass_scale,
        abs(reference.kinetic_energy - candidate.kinetic_energy) / energy_scale,
        momentum_delta / momentum_scale,
    )


def _histogram(
    state: DiskState,
    colors: PassiveColorMap,
    protocol: EchoE1Protocol,
    spatial_grid: tuple[int, int],
    velocity_edges: tuple[float, ...],
    velocity_scale: float,
) -> dict[tuple[int, int, int, int, int], int]:
    histogram: dict[tuple[int, int, int, int, int], int] = defaultdict(int)
    blocks_x, blocks_y = spatial_grid
    for position, velocity, particle_id in zip(
        state.positions, state.velocities, state.particle_ids, strict=True
    ):
        ix, iy = _cell_index(position, protocol, blocks_x, blocks_y)
        vx_bin = bisect_right(velocity_edges, velocity[0] / velocity_scale)
        vy_bin = bisect_right(velocity_edges, velocity[1] / velocity_scale)
        histogram[(ix, iy, colors.label(particle_id), vx_bin, vy_bin)] += 1
    return dict(histogram)


def _cell_moments(
    state: DiskState,
    colors: PassiveColorMap,
    protocol: EchoE1Protocol,
    spatial_grid: tuple[int, int],
) -> dict[tuple[int, int, int], tuple[int, float, float, float, float]]:
    mutable: dict[tuple[int, int, int], list[float]] = defaultdict(
        lambda: [0.0, 0.0, 0.0, 0.0, 0.0]
    )
    blocks_x, blocks_y = spatial_grid
    for position, velocity, particle_id in zip(
        state.positions, state.velocities, state.particle_ids, strict=True
    ):
        ix, iy = _cell_index(position, protocol, blocks_x, blocks_y)
        row = mutable[(ix, iy, colors.label(particle_id))]
        row[0] += 1.0
        row[1] += velocity[0]
        row[2] += velocity[1]
        row[3] += velocity[0] ** 2 + velocity[1] ** 2
        row[4] += velocity[0] ** 2 - velocity[1] ** 2
    return {
        key: (int(row[0]), row[1], row[2], row[3], row[4])
        for key, row in mutable.items()
    }


def _cell_index(
    position: tuple[float, float],
    protocol: EchoE1Protocol,
    blocks_x: int,
    blocks_y: int,
) -> tuple[int, int]:
    x = (position[0] - protocol.domain.lower[0]) / protocol.domain.width
    y = (position[1] - protocol.domain.lower[1]) / protocol.domain.height
    return (
        min(blocks_x - 1, max(0, int(x * blocks_x))),
        min(blocks_y - 1, max(0, int(y * blocks_y))),
    )
