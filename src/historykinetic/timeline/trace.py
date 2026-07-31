"""Turn an ordinary EDMD run into an addressable collision timeline."""

from __future__ import annotations

from historykinetic.solvers import DiskState, Domain2D, HardDiskEDMD
from historykinetic.solvers.result import PairCollisionObservation

from .models import CausalCheckpoint, CausalEvent, TimelineRun, state_sha256


def trace_hard_disk_timeline(
    initial_state: DiskState,
    domain: Domain2D,
    *,
    end_time: float,
    sample_interval: float,
    checkpoint_interval: int = 16,
) -> TimelineRun:
    """Run exact EDMD while recording causal event identities and checkpoints."""

    if checkpoint_interval <= 0:
        raise ValueError("checkpoint_interval must be positive")
    observations: list[PairCollisionObservation] = []
    result = HardDiskEDMD(domain).run(
        initial_state,
        end_time=end_time,
        sample_interval=sample_interval,
        pair_observer=observations.append,
    )
    latest_event_by_particle: dict[int, str] = {}
    events: list[CausalEvent] = []
    checkpoints = [
        CausalCheckpoint(
            checkpoint_id="checkpoint-initial",
            kind="initial",
            time=0.0,
            last_event_ordinal=-1,
            state=initial_state.copy(),
            state_sha256=state_sha256(initial_state),
        )
    ]
    for observation in observations:
        collision = observation.event
        event_id = f"collision-{observation.ordinal:06d}"
        parents = {
            latest_event_by_particle[particle]
            for particle in (collision.particle_a, collision.particle_b)
            if particle in latest_event_by_particle
        }
        event = CausalEvent(
            event_id=event_id,
            ordinal=observation.ordinal,
            queue_sequence=observation.queue_sequence,
            time=collision.time,
            particle_a=collision.particle_a,
            particle_b=collision.particle_b,
            contact_normal=collision.contact_normal or (0.0, 0.0),
            incoming_relative_normal_velocity=(
                collision.incoming_relative_normal_velocity or 0.0
            ),
            predecessors=tuple(sorted(parents)),
            pre_state_sha256=state_sha256(observation.state_before),
            post_state_sha256=state_sha256(observation.state_after),
        )
        events.append(event)
        latest_event_by_particle[collision.particle_a] = event_id
        latest_event_by_particle[collision.particle_b] = event_id
        if (observation.ordinal + 1) % checkpoint_interval == 0:
            checkpoints.append(
                CausalCheckpoint(
                    checkpoint_id=f"checkpoint-event-{observation.ordinal:06d}",
                    kind="periodic",
                    time=collision.time,
                    last_event_ordinal=observation.ordinal,
                    state=observation.state_after.copy(),
                    state_sha256=event.post_state_sha256,
                )
            )

    terminal = result.snapshots[-1]
    checkpoints.append(
        CausalCheckpoint(
            checkpoint_id="checkpoint-terminal",
            kind="terminal",
            time=terminal.time,
            last_event_ordinal=len(events) - 1,
            state=terminal.state.copy(),
            state_sha256=state_sha256(terminal.state),
        )
    )
    return TimelineRun(
        initial_state=initial_state.copy(),
        result=result,
        events=tuple(events),
        checkpoints=tuple(checkpoints),
        checkpoint_interval=checkpoint_interval,
    )


def checkpoint_at_time(
    timeline: TimelineRun,
    domain: Domain2D,
    *,
    time: float,
) -> CausalCheckpoint:
    """Materialize an exact forced checkpoint at a branch time."""

    if not 0.0 < time <= timeline.result.snapshots[-1].time:
        raise ValueError("checkpoint time must lie inside the timeline horizon")
    prefix = HardDiskEDMD(domain).run(
        timeline.initial_state,
        end_time=time,
        sample_interval=time,
    )
    last_ordinal = sum(event.time <= time for event in timeline.events) - 1
    state = prefix.snapshots[-1].state
    return CausalCheckpoint(
        checkpoint_id=f"checkpoint-fork-{time:.12f}",
        kind="fork",
        time=time,
        last_event_ordinal=last_ordinal,
        state=state.copy(),
        state_sha256=state_sha256(state),
    )

