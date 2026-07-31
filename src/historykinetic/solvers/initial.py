"""Deterministic initial ensembles shared by exact and kinetic references."""

from __future__ import annotations

import random
from math import ceil, floor, pi, sqrt

from historykinetic.solvers.state import DiskState, Domain2D, Vec2, validate_state_geometry


def particle_count_from_packing_fraction(
    domain: Domain2D,
    *,
    radius: float,
    packing_fraction: float,
) -> int:
    if not 0 < packing_fraction < 1:
        raise ValueError("packing_fraction must lie in (0, 1)")
    count = round(packing_fraction * domain.area / (pi * radius * radius))
    return max(2, count)


def make_initial_state(
    domain: Domain2D,
    *,
    particle_count: int,
    radius: float,
    mass: float,
    temperature: float,
    mean_velocity: Vec2 = (0.0, 0.0),
    seed: int = 0,
    kind: str = "maxwellian",
    stream_speed: float = 1.0,
) -> DiskState:
    if particle_count < 2:
        raise ValueError("particle_count must be at least two")
    if radius <= 0 or mass <= 0 or temperature < 0:
        raise ValueError("radius/mass must be positive and temperature non-negative")

    rng = random.Random(seed)
    positions = _non_overlapping_grid_positions(
        domain,
        particle_count=particle_count,
        radius=radius,
        rng=rng,
    )
    velocities = _velocities(
        particle_count,
        mass=mass,
        temperature=temperature,
        mean_velocity=mean_velocity,
        kind=kind,
        stream_speed=stream_speed,
        rng=rng,
    )
    state = DiskState(
        positions=positions,
        velocities=velocities,
        radii=[radius] * particle_count,
        masses=[mass] * particle_count,
        particle_ids=list(range(particle_count)),
        weights=[1.0] * particle_count,
    )
    validate_state_geometry(state, domain)
    return state


def _non_overlapping_grid_positions(
    domain: Domain2D,
    *,
    particle_count: int,
    radius: float,
    rng: random.Random,
) -> list[Vec2]:
    usable_width = (
        domain.width
        if domain.boundary.value == "periodic"
        else domain.width - 2 * radius
    )
    usable_height = (
        domain.height if domain.boundary.value == "periodic" else domain.height - 2 * radius
    )
    if usable_width <= 0 or usable_height <= 0:
        raise ValueError("particle radius leaves no usable domain")

    aspect = usable_width / usable_height
    nx = max(1, ceil(sqrt(particle_count * aspect)))
    ny = max(1, ceil(particle_count / nx))

    while True:
        spacing_x = usable_width / nx
        spacing_y = usable_height / ny
        if min(spacing_x, spacing_y) > 2.05 * radius:
            break
        if spacing_x < spacing_y:
            nx += 1
        else:
            ny += 1
        if nx * ny > 100 * particle_count:
            raise ValueError("unable to place particles without overlap")

    origin_x = domain.lower[0] if domain.boundary.value == "periodic" else domain.lower[0] + radius
    origin_y = domain.lower[1] if domain.boundary.value == "periodic" else domain.lower[1] + radius
    candidates: list[Vec2] = []
    jitter_scale = 0.12 * min(spacing_x - 2 * radius, spacing_y - 2 * radius)
    for iy in range(ny):
        for ix in range(nx):
            x = origin_x + (ix + 0.5) * spacing_x
            y = origin_y + (iy + 0.5) * spacing_y
            if jitter_scale > 0:
                x += rng.uniform(-jitter_scale, jitter_scale)
                y += rng.uniform(-jitter_scale, jitter_scale)
            position = domain.wrap((x, y))
            if domain.boundary.value == "periodic" or domain.contains_disk(position, radius):
                candidates.append(position)

    if len(candidates) < particle_count:
        # Obstacles may remove grid sites.  Retry on successively finer grids.
        for multiplier in range(2, 7):
            candidates = []
            fine_nx = nx * multiplier
            fine_ny = ny * multiplier
            for iy in range(fine_ny):
                for ix in range(fine_nx):
                    position = (
                        domain.lower[0]
                        + radius
                        + (ix + 0.5) * (domain.width - 2 * radius) / fine_nx,
                        domain.lower[1]
                        + radius
                        + (iy + 0.5) * (domain.height - 2 * radius) / fine_ny,
                    )
                    if not domain.contains_disk(position, radius):
                        continue
                    if all(
                        (position[0] - other[0]) ** 2 + (position[1] - other[1]) ** 2
                        >= (2.05 * radius) ** 2
                        for other in candidates
                    ):
                        candidates.append(position)
            if len(candidates) >= particle_count:
                break
    if len(candidates) < particle_count:
        raise ValueError(
            f"geometry contains only {len(candidates)} safe grid sites "
            f"for {particle_count} particles"
        )
    rng.shuffle(candidates)
    return candidates[:particle_count]


def _velocities(
    particle_count: int,
    *,
    mass: float,
    temperature: float,
    mean_velocity: Vec2,
    kind: str,
    stream_speed: float,
    rng: random.Random,
) -> list[Vec2]:
    thermal_sigma = sqrt(temperature / mass) if temperature > 0 else 0.0
    raw: list[Vec2] = []
    if kind == "maxwellian":
        raw = [
            (rng.gauss(0.0, thermal_sigma), rng.gauss(0.0, thermal_sigma))
            for _ in range(particle_count)
        ]
    elif kind in {"two_stream", "bimodal"}:
        raw = [
            (
                (-stream_speed if index % 2 == 0 else stream_speed)
                + rng.gauss(0.0, 0.25 * thermal_sigma),
                rng.gauss(0.0, thermal_sigma),
            )
            for index in range(particle_count)
        ]
    else:
        raise ValueError(f"unsupported initial velocity kind: {kind}")

    raw_mean = (
        sum(velocity[0] for velocity in raw) / particle_count,
        sum(velocity[1] for velocity in raw) / particle_count,
    )
    centered = [
        (velocity[0] - raw_mean[0], velocity[1] - raw_mean[1]) for velocity in raw
    ]
    current_temperature = (
        mass
        * sum(vx * vx + vy * vy for vx, vy in centered)
        / (2.0 * particle_count)
    )
    if temperature == 0:
        scale = 0.0
    elif current_temperature <= 0:
        raise ValueError("cannot rescale a zero-temperature sample")
    else:
        scale = sqrt(temperature / current_temperature)
    return [
        (
            mean_velocity[0] + scale * velocity[0],
            mean_velocity[1] + scale * velocity[1],
        )
        for velocity in centered
    ]


def lattice_capacity(domain: Domain2D, radius: float) -> int:
    """Conservative rectangular-grid capacity, useful for case validation."""

    return max(0, floor(domain.width / (2.05 * radius))) * max(
        0, floor(domain.height / (2.05 * radius))
    )
