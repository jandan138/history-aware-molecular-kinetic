from __future__ import annotations

from math import hypot

from historykinetic.echo import prepare_echo_initial_state, reverse_state
from historykinetic.echo.audit import color_score
from historykinetic.solvers import Domain2D, HardDiskEDMD
from historykinetic.solvers.state import minimum_image
from historykinetic.timeline import (
    CollisionCausalGraph,
    PairRelativeVelocityRotationEdit,
    checkpoint_at_time,
    fork_causal_branch,
    trace_hard_disk_timeline,
)

from .models import E3Metrics, MolecularTimeMachineE3Result
from .protocol import MolecularTimeMachineE3Protocol


def run_molecular_time_machine_e3(
    protocol: MolecularTimeMachineE3Protocol,
) -> MolecularTimeMachineE3Result:
    e1 = protocol.e1_protocol
    initial_state, colors = prepare_echo_initial_state(
        e1,
        particle_count=protocol.hero.particle_count,
        seed=protocol.hero.seed,
    )
    preparation = HardDiskEDMD(e1.domain).run(
        initial_state,
        end_time=e1.preparation_time,
        sample_interval=protocol.sample_interval,
    )
    reversed_pivot = reverse_state(preparation.snapshots[-1].state)
    timeline = trace_hard_disk_timeline(
        reversed_pivot,
        e1.domain,
        end_time=protocol.end_time,
        sample_interval=protocol.sample_interval,
        checkpoint_interval=protocol.checkpoint_interval_events,
    )
    target = timeline.event(protocol.hero.target_collision_ordinal)
    if target.pair != protocol.hero.expected_pair:
        raise RuntimeError(
            f"frozen target pair drifted: expected {protocol.hero.expected_pair}, got {target.pair}"
        )
    if abs(target.time - protocol.hero.expected_time) > protocol.hero.recipe_tolerance:
        raise RuntimeError(
            "frozen target time drifted: "
            f"expected {protocol.hero.expected_time}, got {target.time}"
        )
    checkpoint = checkpoint_at_time(
        timeline,
        e1.domain,
        time=target.time - protocol.fork_lead_time,
    )
    branch = fork_causal_branch(
        timeline,
        e1.domain,
        checkpoint=checkpoint,
        edit=PairRelativeVelocityRotationEdit(
            particle_a=target.particle_a,
            particle_b=target.particle_b,
            angle_degrees=protocol.edit_angle_degrees,
        ),
        end_time=protocol.end_time,
        sample_interval=protocol.sample_interval,
    )
    baseline_terminal = timeline.result.snapshots[-1].state
    edited_terminal = branch.local.simulation.snapshots[-1].state
    baseline_score = color_score(baseline_terminal, colors, e1)
    edited_score = color_score(edited_terminal, colors, e1)
    visibly_changed = sum(
        _periodic_distance(left, right, e1.domain)
        > protocol.visible_position_threshold
        for left, right in zip(
            baseline_terminal.positions,
            edited_terminal.positions,
            strict=True,
        )
    )
    descendants = CollisionCausalGraph(timeline.events).descendant_particles(target.event_id)
    metrics = E3Metrics(
        baseline_terminal_color_score=baseline_score,
        edited_terminal_color_score=edited_score,
        terminal_color_gap=baseline_score - edited_score,
        visibly_changed_particle_count=visibly_changed,
        visibly_changed_particle_fraction=visibly_changed / protocol.hero.particle_count,
        baseline_graph_descendant_particle_count=len(descendants),
        baseline_graph_descendant_particle_fraction=(
            len(descendants) / protocol.hero.particle_count
        ),
    )
    return MolecularTimeMachineE3Result(
        protocol=protocol,
        colors=colors,
        preparation=preparation,
        timeline=timeline,
        target_event=target,
        fork_checkpoint=checkpoint,
        branch=branch,
        metrics=metrics,
    )


def _periodic_distance(
    left: tuple[float, float],
    right: tuple[float, float],
    domain: Domain2D,
) -> float:
    displacement = minimum_image((right[0] - left[0], right[1] - left[1]), domain)
    return hypot(*displacement)
