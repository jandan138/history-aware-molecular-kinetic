"""Public data types for an addressable collision timeline."""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass

from historykinetic.solvers import DiskState, SimulationResult


def state_sha256(state: DiskState) -> str:
    """Hash a complete particle state without lossy text serialization."""

    digest = hashlib.sha256()
    digest.update(struct.pack("!Q", state.particle_count))
    for particle_id, position, velocity, radius, mass, weight in zip(
        state.particle_ids,
        state.positions,
        state.velocities,
        state.radii,
        state.masses,
        state.weights,
        strict=True,
    ):
        digest.update(struct.pack("!q7d", particle_id, *position, *velocity, radius, mass, weight))
    return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class CausalEvent:
    """One accepted pair collision with stable identity and causal parents."""

    event_id: str
    ordinal: int
    queue_sequence: int
    time: float
    particle_a: int
    particle_b: int
    contact_normal: tuple[float, float]
    incoming_relative_normal_velocity: float
    predecessors: tuple[str, ...]
    pre_state_sha256: str
    post_state_sha256: str

    @property
    def pair(self) -> tuple[int, int]:
        return (self.particle_a, self.particle_b)


@dataclass(frozen=True, slots=True)
class CausalCheckpoint:
    """Exact restart state at an initial, periodic, fork, or terminal boundary."""

    checkpoint_id: str
    kind: str
    time: float
    last_event_ordinal: int
    state: DiskState
    state_sha256: str


@dataclass(frozen=True, slots=True)
class TimelineRun:
    """A conventional EDMD result augmented with its collision history."""

    initial_state: DiskState
    result: SimulationResult
    events: tuple[CausalEvent, ...]
    checkpoints: tuple[CausalCheckpoint, ...]
    checkpoint_interval: int

    def event(self, ordinal_or_id: int | str) -> CausalEvent:
        if isinstance(ordinal_or_id, int):
            try:
                return self.events[ordinal_or_id]
            except IndexError as error:
                raise KeyError(f"unknown collision ordinal: {ordinal_or_id}") from error
        for event in self.events:
            if event.event_id == ordinal_or_id:
                return event
        raise KeyError(f"unknown collision event: {ordinal_or_id}")


@dataclass(frozen=True, slots=True)
class CollisionCausalGraph:
    """Queryable DAG induced by each particle's preceding collision."""

    events: tuple[CausalEvent, ...]

    def __post_init__(self) -> None:
        event_ids = [event.event_id for event in self.events]
        if len(event_ids) != len(set(event_ids)):
            raise ValueError("causal event IDs must be unique")

    def event(self, event_id: str) -> CausalEvent:
        for event in self.events:
            if event.event_id == event_id:
                return event
        raise KeyError(f"unknown collision event: {event_id}")

    def predecessors(self, event_id: str) -> tuple[CausalEvent, ...]:
        return tuple(self.event(parent) for parent in self.event(event_id).predecessors)

    def successors(self, event_id: str) -> tuple[CausalEvent, ...]:
        return tuple(event for event in self.events if event_id in event.predecessors)

    def descendants(self, event_id: str) -> tuple[CausalEvent, ...]:
        """Return downstream events in deterministic timeline order."""

        seen: set[str] = set()
        frontier = [event_id]
        while frontier:
            parent = frontier.pop()
            for child in self.successors(parent):
                if child.event_id not in seen:
                    seen.add(child.event_id)
                    frontier.append(child.event_id)
        return tuple(event for event in self.events if event.event_id in seen)

    def descendant_particles(self, event_id: str) -> tuple[int, ...]:
        root = self.event(event_id)
        particles = {root.particle_a, root.particle_b}
        for event in self.descendants(event_id):
            particles.update(event.pair)
        return tuple(sorted(particles))

