"""Physically conservative edits applied at a collision-timeline fork."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, hypot, radians, sin

from historykinetic.solvers import DiskState


@dataclass(frozen=True, slots=True)
class PairRelativeVelocityRotationEdit:
    """Rotate one pair's relative velocity in its center-of-mass frame."""

    particle_a: int
    particle_b: int
    angle_degrees: float

    @property
    def pair(self) -> tuple[int, int]:
        return (self.particle_a, self.particle_b)


@dataclass(frozen=True, slots=True)
class EditAudit:
    momentum_error: float
    energy_error: float
    relative_energy_error: float


def apply_pair_relative_velocity_rotation(
    state: DiskState,
    edit: PairRelativeVelocityRotationEdit,
) -> tuple[DiskState, EditAudit]:
    """Apply ``edit`` without changing pair momentum or kinetic energy."""

    if edit.particle_a == edit.particle_b:
        raise ValueError("a pair edit requires two distinct particles")
    index_by_id = {particle_id: index for index, particle_id in enumerate(state.particle_ids)}
    try:
        left = index_by_id[edit.particle_a]
        right = index_by_id[edit.particle_b]
    except KeyError as error:
        raise KeyError(f"edit particle is absent from checkpoint: {error.args[0]}") from error

    edited = state.copy()
    momentum_before = edited.momentum
    energy_before = edited.kinetic_energy
    mass_a = edited.masses[left]
    mass_b = edited.masses[right]
    velocity_a = edited.velocities[left]
    velocity_b = edited.velocities[right]
    total_mass = mass_a + mass_b
    center = (
        (mass_a * velocity_a[0] + mass_b * velocity_b[0]) / total_mass,
        (mass_a * velocity_a[1] + mass_b * velocity_b[1]) / total_mass,
    )
    relative = (velocity_a[0] - velocity_b[0], velocity_a[1] - velocity_b[1])
    angle = radians(edit.angle_degrees)
    rotated = (
        cos(angle) * relative[0] - sin(angle) * relative[1],
        sin(angle) * relative[0] + cos(angle) * relative[1],
    )
    edited.velocities[left] = (
        center[0] + mass_b * rotated[0] / total_mass,
        center[1] + mass_b * rotated[1] / total_mass,
    )
    edited.velocities[right] = (
        center[0] - mass_a * rotated[0] / total_mass,
        center[1] - mass_a * rotated[1] / total_mass,
    )

    momentum_after = edited.momentum
    energy_after = edited.kinetic_energy
    momentum_error = hypot(
        momentum_after[0] - momentum_before[0],
        momentum_after[1] - momentum_before[1],
    )
    energy_error = abs(energy_after - energy_before)
    return edited, EditAudit(
        momentum_error=momentum_error,
        energy_error=energy_error,
        relative_energy_error=energy_error / max(abs(energy_before), 1.0e-30),
    )

