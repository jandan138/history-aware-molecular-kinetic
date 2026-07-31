"""Shared deterministic hard-disk collision primitives.

The reference EDMD solver and the causal branch executor deliberately call the
same prediction, advection, and impulse functions.  Keeping one numerical
kernel is what makes a branch comparison meaningful: a mismatch then points to
branch scheduling, rather than to two slightly different physics formulas.
"""

from __future__ import annotations

from collections.abc import Callable
from math import ceil, floor, hypot, sqrt

from historykinetic.contracts import CollisionEvent
from historykinetic.solvers.state import BoundaryKind, DiskState, Domain2D

TIME_EPS = 1.0e-12
CONTACT_EPS = 1.0e-10


def predict_pair_collision(
    state: DiskState,
    domain: Domain2D,
    left: int,
    right: int,
    horizon: float,
) -> tuple[float, tuple[float, float]] | None:
    """Return the next exact pair-contact time and normal, if one exists."""

    pa = state.positions[left]
    pb = state.positions[right]
    va = state.velocities[left]
    vb = state.velocities[right]
    dv = (vb[0] - va[0], vb[1] - va[1])
    speed2 = dv[0] * dv[0] + dv[1] * dv[1]
    if speed2 <= TIME_EPS:
        return None
    contact = state.radii[left] + state.radii[right]

    shifts_x: tuple[int, ...] = (0,)
    shifts_y: tuple[int, ...] = (0,)
    if domain.boundary is BoundaryKind.PERIODIC:
        shifts_x = periodic_shift_range(pb[0] - pa[0], dv[0], domain.width, horizon)
        shifts_y = periodic_shift_range(pb[1] - pa[1], dv[1], domain.height, horizon)

    best: tuple[float, tuple[float, float]] | None = None
    for shift_x in shifts_x:
        for shift_y in shifts_y:
            rx = pb[0] - pa[0] + shift_x * domain.width
            ry = pb[1] - pa[1] + shift_y * domain.height
            b = rx * dv[0] + ry * dv[1]
            c = rx * rx + ry * ry - contact * contact
            if c < -CONTACT_EPS:
                raise RuntimeError(
                    "overlap detected while scheduling particles "
                    f"{state.particle_ids[left]} and {state.particle_ids[right]}"
                )
            if b >= -TIME_EPS:
                continue
            discriminant = b * b - speed2 * c
            if discriminant <= 0:
                continue
            dt = (-b - sqrt(discriminant)) / speed2
            if dt <= TIME_EPS or dt > horizon + TIME_EPS:
                continue
            cx = rx + dv[0] * dt
            cy = ry + dv[1] * dt
            distance = hypot(cx, cy)
            if distance <= 0:
                continue
            candidate = (dt, (cx / distance, cy / distance))
            if best is None or candidate[0] < best[0]:
                best = candidate
    return best


def advance_state(state: DiskState, domain: Domain2D, dt: float) -> None:
    """Advance all particles ballistically by ``dt`` in place."""

    if dt < -TIME_EPS:
        raise RuntimeError("cannot advance state backward")
    if dt <= 0:
        return
    state.positions = [
        domain.wrap(
            (
                position[0] + velocity[0] * dt,
                position[1] + velocity[1] * dt,
            )
        )
        for position, velocity in zip(state.positions, state.velocities, strict=True)
    ]


def resolve_pair_collision(
    state: DiskState,
    domain: Domain2D,
    *,
    left: int,
    right: int,
    normal: tuple[float, float],
    time: float,
    block_locator: Callable[[tuple[float, float]], str] | None = None,
) -> CollisionEvent:
    """Apply the elastic impulse and return the public collision record."""

    va = state.velocities[left]
    vb = state.velocities[right]
    pre_a = (va[0], va[1], 0.0)
    pre_b = (vb[0], vb[1], 0.0)
    relative_normal_speed = (va[0] - vb[0]) * normal[0] + (
        va[1] - vb[1]
    ) * normal[1]
    if relative_normal_speed < -1.0e-9:
        raise RuntimeError("valid collision event is separating")
    inverse_mass = 1.0 / state.masses[left] + 1.0 / state.masses[right]
    impulse = 2.0 * relative_normal_speed / inverse_mass
    state.velocities[left] = (
        va[0] - impulse * normal[0] / state.masses[left],
        va[1] - impulse * normal[1] / state.masses[left],
    )
    state.velocities[right] = (
        vb[0] + impulse * normal[0] / state.masses[right],
        vb[1] + impulse * normal[1] / state.masses[right],
    )
    post_a = (*state.velocities[left], 0.0)
    post_b = (*state.velocities[right], 0.0)
    contact_point = domain.wrap(
        (
            state.positions[left][0] + normal[0] * state.radii[left],
            state.positions[left][1] + normal[1] * state.radii[left],
        )
    )
    block_id = block_locator(contact_point) if block_locator is not None else "domain"
    return CollisionEvent(
        time=time,
        particle_a=state.particle_ids[left],
        particle_b=state.particle_ids[right],
        block_id=block_id,
        pre_velocity_a=pre_a,
        pre_velocity_b=pre_b,
        post_velocity_a=post_a,
        post_velocity_b=post_b,
        contact_normal=normal,
        incoming_relative_normal_velocity=relative_normal_speed,
    )


def periodic_shift_range(
    displacement: float,
    relative_velocity: float,
    period: float,
    horizon: float,
) -> tuple[int, ...]:
    start = displacement
    finish = displacement + relative_velocity * max(0.0, horizon)
    low = min(start, finish)
    high = max(start, finish)
    minimum = floor(-high / period) - 1
    maximum = ceil(-low / period) + 1
    return tuple(range(minimum, maximum + 1))
