"""Resolved-present-preserving velocity-ownership surgery."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from math import hypot

from historykinetic.solvers import DiskState, Domain2D, validate_state_geometry

from .models import ResolvedPresentAudit, VelocityOwnershipSurgery


def enumerate_target_surgeries(
    state: DiskState,
    domain: Domain2D,
    *,
    pivot_time: float,
    target_particle_ids: tuple[int, ...],
    declared_spatial_grid: tuple[int, int],
    maximum_disjoint_swaps: int,
) -> tuple[VelocityOwnershipSurgery, ...]:
    """Enumerate the compact E5 palette of legal within-cell target swaps."""

    index_by_id = {particle_id: index for index, particle_id in enumerate(state.particle_ids)}
    groups: dict[tuple[int, int], list[int]] = defaultdict(list)
    for particle_id in target_particle_ids:
        try:
            position = state.positions[index_by_id[particle_id]]
        except KeyError as error:
            raise KeyError(f"target particle is absent from pivot: {particle_id}") from error
        groups[_cell_index(position, domain, declared_spatial_grid)].append(particle_id)

    atomic_swaps = tuple(
        pair
        for cell in sorted(groups)
        for pair in combinations(sorted(groups[cell]), 2)
    )
    surgeries: list[VelocityOwnershipSurgery] = []
    for swap_count in range(1, maximum_disjoint_swaps + 1):
        for swaps in combinations(atomic_swaps, swap_count):
            touched = [particle_id for pair in swaps for particle_id in pair]
            if len(touched) != len(set(touched)):
                continue
            surgeries.append(
                VelocityOwnershipSurgery(
                    pivot_time=pivot_time,
                    declared_spatial_grid=declared_spatial_grid,
                    swaps=tuple(sorted(swaps)),
                )
            )
    return tuple(surgeries)


def apply_velocity_ownership_surgery(
    state: DiskState,
    domain: Domain2D,
    surgery: VelocityOwnershipSurgery,
    *,
    target_particle_ids: tuple[int, ...],
) -> tuple[DiskState, ResolvedPresentAudit]:
    """Swap velocity ownership without moving or relabeling any particle."""

    index_by_id = {particle_id: index for index, particle_id in enumerate(state.particle_ids)}
    target_set = set(target_particle_ids)
    edited = state.copy()
    before_momentum = state.momentum
    before_energy = state.kinetic_energy
    before_mass = state.total_mass
    for left_id, right_id in surgery.swaps:
        if left_id not in target_set or right_id not in target_set:
            raise ValueError("E5 surgery may touch only creator-selected target particles")
        try:
            left = index_by_id[left_id]
            right = index_by_id[right_id]
        except KeyError as error:
            raise KeyError(f"surgery particle is absent from pivot: {error.args[0]}") from error
        left_cell = _cell_index(
            state.positions[left], domain, surgery.declared_spatial_grid
        )
        right_cell = _cell_index(
            state.positions[right], domain, surgery.declared_spatial_grid
        )
        if left_cell != right_cell:
            raise ValueError("E5 velocity ownership may be exchanged only within one cell")
        edited.velocities[left], edited.velocities[right] = (
            edited.velocities[right],
            edited.velocities[left],
        )

    geometry_valid = True
    try:
        validate_state_geometry(edited, domain)
    except ValueError:
        geometry_valid = False
    arrays_equal = (
        state.positions == edited.positions
        and state.radii == edited.radii
        and state.masses == edited.masses
        and state.particle_ids == edited.particle_ids
        and state.weights == edited.weights
    )
    audit = ResolvedPresentAudit(
        positions_identical=state.positions == edited.positions,
        colors_identical=True,
        particle_arrays_identical_except_velocity_ownership=arrays_equal,
        declared_cell_velocity_multisets_identical=(
            _cell_velocity_multisets(state, domain, surgery.declared_spatial_grid)
            == _cell_velocity_multisets(edited, domain, surgery.declared_spatial_grid)
        ),
        declared_cell_target_velocity_multisets_identical=(
            _cell_velocity_multisets(
                state,
                domain,
                surgery.declared_spatial_grid,
                particle_ids=target_set,
            )
            == _cell_velocity_multisets(
                edited,
                domain,
                surgery.declared_spatial_grid,
                particle_ids=target_set,
            )
        ),
        geometry_valid=geometry_valid,
        mass_error=abs(edited.total_mass - before_mass),
        momentum_error=hypot(
            edited.momentum[0] - before_momentum[0],
            edited.momentum[1] - before_momentum[1],
        ),
        energy_error=abs(edited.kinetic_energy - before_energy),
    )
    return edited, audit


def _cell_velocity_multisets(
    state: DiskState,
    domain: Domain2D,
    grid: tuple[int, int],
    *,
    particle_ids: set[int] | None = None,
) -> dict[tuple[int, int], tuple[tuple[float, float], ...]]:
    mutable: dict[tuple[int, int], list[tuple[float, float]]] = defaultdict(list)
    for particle_id, position, velocity in zip(
        state.particle_ids, state.positions, state.velocities, strict=True
    ):
        if particle_ids is not None and particle_id not in particle_ids:
            continue
        mutable[_cell_index(position, domain, grid)].append(velocity)
    return {cell: tuple(sorted(velocities)) for cell, velocities in mutable.items()}


def _cell_index(
    position: tuple[float, float],
    domain: Domain2D,
    grid: tuple[int, int],
) -> tuple[int, int]:
    blocks_x, blocks_y = grid
    normalized_x = (position[0] - domain.lower[0]) / domain.width
    normalized_y = (position[1] - domain.lower[1]) / domain.height
    return (
        min(blocks_x - 1, max(0, int(normalized_x * blocks_x))),
        min(blocks_y - 1, max(0, int(normalized_y * blocks_y))),
    )
