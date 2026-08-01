"""Run the registered E4 causal-steering authoring session."""

from __future__ import annotations

from statistics import median

from historykinetic.echo import prepare_echo_initial_state, reverse_state
from historykinetic.echo.audit import color_score
from historykinetic.echo.models import PassiveColorMap
from historykinetic.solvers import DiskState, HardDiskEDMD
from historykinetic.timeline import (
    CausalEvent,
    CollisionCausalGraph,
    PairRelativeVelocityRotationEdit,
    TimelineRun,
    checkpoint_at_time,
    fork_causal_branch,
    preview_causal_branch,
    trace_hard_disk_timeline,
)

from .models import (
    CausalCandidate,
    CausalTarget,
    E4Metrics,
    MolecularTimeMachineE4Result,
    PalettePreview,
    TargetChangeMetrics,
)
from .protocol import MolecularTimeMachineE4Protocol

_PORTABLE_EVENT_LOCATOR_TOLERANCE = 1.0e-9


def run_molecular_time_machine_e4(
    protocol: MolecularTimeMachineE4Protocol,
) -> MolecularTimeMachineE4Result:
    """Execute one compact outcome-to-cause authoring session.

    Candidate ranking sees only the unedited terminal target and the baseline
    collision DAG.  It does not inspect any edited outcome.  The small angle
    palette is then a creator-facing set of exact local previews; only the one
    saved choice launches the full-resimulation oracle.
    """

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
    target = _resolve_target(protocol, timeline, colors)
    candidates = _rank_candidates(protocol, timeline, target)
    _validate_ranked_hero(protocol, candidates)

    palette: list[PalettePreview] = []
    checkpoints = {}
    for candidate in candidates:
        checkpoint = checkpoint_at_time(
            timeline,
            e1.domain,
            time=candidate.event.time - protocol.fork_lead_time,
        )
        checkpoints[candidate.event.event_id] = checkpoint
        for angle_degrees in protocol.palette_angles_degrees:
            preview = preview_causal_branch(
                timeline,
                e1.domain,
                checkpoint=checkpoint,
                edit=PairRelativeVelocityRotationEdit(
                    particle_a=candidate.event.particle_a,
                    particle_b=candidate.event.particle_b,
                    angle_degrees=angle_degrees,
                ),
                end_time=protocol.end_time,
                sample_interval=protocol.sample_interval,
            )
            palette.append(
                PalettePreview(
                    candidate=candidate,
                    angle_degrees=angle_degrees,
                    preview=preview,
                    target_metrics=_target_change_metrics(
                        protocol,
                        timeline,
                        target,
                        preview.local.simulation.snapshots[-1].state,
                    ),
                )
            )

    recommended = candidates[0]
    selected_preview = _select_angle_for_recommended_collision(
        tuple(palette), recommended.event.event_id
    )
    selected_checkpoint = checkpoints[recommended.event.event_id]
    selected_branch = fork_causal_branch(
        timeline,
        e1.domain,
        checkpoint=selected_checkpoint,
        edit=PairRelativeVelocityRotationEdit(
            particle_a=recommended.event.particle_a,
            particle_b=recommended.event.particle_b,
            angle_degrees=selected_preview.angle_degrees,
        ),
        end_time=protocol.end_time,
        sample_interval=protocol.sample_interval,
    )
    selected_target_metrics = _target_change_metrics(
        protocol,
        timeline,
        target,
        selected_branch.local.simulation.snapshots[-1].state,
    )
    if selected_target_metrics != selected_preview.target_metrics:
        raise RuntimeError("saved E4 branch drifted from its exact local preview")

    metrics = E4Metrics(
        baseline_terminal_color_score=color_score(
            timeline.result.snapshots[-1].state,
            colors,
            e1,
        ),
        selected_candidate_rank=recommended.rank,
        selected_candidate_causal_score=recommended.causal_score,
        selected_angle_degrees=selected_preview.angle_degrees,
        preview_count=len(palette),
        preview_median_seconds=median(item.preview.local_seconds for item in palette),
        target_particle_count=len(target.particle_ids),
        collateral_foreground_particle_count=len(target.collateral_foreground_particle_ids),
        target_ejection_fraction=selected_target_metrics.target_ejection_fraction,
        collateral_ejection_fraction=selected_target_metrics.collateral_ejection_fraction,
        target_to_collateral_ratio=selected_target_metrics.target_to_collateral_ratio,
        selected_branch_reuse_fraction=(
            selected_branch.local.diagnostics.baseline_event_reuse_fraction
        ),
        selected_branch_peak_affected_fraction=(
            selected_branch.local.diagnostics.peak_affected_fraction
        ),
    )
    return MolecularTimeMachineE4Result(
        protocol=protocol,
        colors=colors,
        preparation=preparation,
        timeline=timeline,
        target=target,
        candidates=candidates,
        palette=tuple(palette),
        selected_preview=selected_preview,
        selected_checkpoint=selected_checkpoint,
        selected_branch=selected_branch,
        metrics=metrics,
    )


def _resolve_target(
    protocol: MolecularTimeMachineE4Protocol,
    timeline: TimelineRun,
    colors: PassiveColorMap,
) -> CausalTarget:
    terminal = timeline.result.snapshots[-1].state
    x_bounds = protocol.hero.target_x_bounds
    y_bounds = protocol.hero.target_y_bounds
    target_ids = tuple(
        particle_id
        for particle_id, position in zip(terminal.particle_ids, terminal.positions, strict=True)
        if colors.label(particle_id) == 1 and _inside_bounds(position, x_bounds, y_bounds)
    )
    if not target_ids:
        raise RuntimeError("E4 target selection contains no foreground particles")
    if target_ids != protocol.hero.expected_target_particle_ids:
        raise RuntimeError(
            "frozen E4 target membership drifted: "
            f"expected {protocol.hero.expected_target_particle_ids}, got {target_ids}"
        )
    target_set = set(target_ids)
    collateral = tuple(
        particle_id
        for particle_id in terminal.particle_ids
        if colors.label(particle_id) == 1 and particle_id not in target_set
    )
    return CausalTarget(
        target_id=protocol.hero.target_id,
        description=protocol.hero.target_description,
        x_bounds=x_bounds,
        y_bounds=y_bounds,
        particle_ids=target_ids,
        collateral_foreground_particle_ids=collateral,
    )


def _rank_candidates(
    protocol: MolecularTimeMachineE4Protocol,
    timeline: TimelineRun,
    target: CausalTarget,
) -> tuple[CausalCandidate, ...]:
    events = timeline.events
    graph = CollisionCausalGraph(events)
    target_ids = set(target.particle_ids)
    scored: list[tuple[float, float, float, CausalEvent, tuple[int, ...], tuple[int, ...]]] = []
    for event in events[: protocol.ranking.candidate_event_limit]:
        descendants = graph.descendant_particles(event.event_id)
        target_descendants = tuple(
            particle_id for particle_id in descendants if particle_id in target_ids
        )
        coverage = len(target_descendants) / len(target.particle_ids)
        purity = len(target_descendants) / len(descendants)
        causal_score = _harmonic_mean(coverage, purity)
        scored.append((causal_score, coverage, purity, event, descendants, target_descendants))
    scored.sort(key=lambda item: (-item[0], -item[1], -item[2], item[3].ordinal))
    return tuple(
        CausalCandidate(
            rank=rank,
            event=event,
            descendant_particle_ids=descendants,
            target_descendant_particle_ids=target_descendants,
            coverage=coverage,
            purity=purity,
            causal_score=causal_score,
        )
        for rank, (
            causal_score,
            coverage,
            purity,
            event,
            descendants,
            target_descendants,
        ) in enumerate(scored[: protocol.ranking.shortlist_size], start=1)
    )


def _validate_ranked_hero(
    protocol: MolecularTimeMachineE4Protocol,
    candidates: tuple[CausalCandidate, ...],
) -> None:
    if not candidates:
        raise RuntimeError("E4 causal ranking produced no candidates")
    recommended = candidates[0].event
    expected = protocol.hero
    if recommended.ordinal != expected.expected_recommended_collision_ordinal:
        raise RuntimeError(
            "frozen E4 recommendation drifted: "
            f"expected ordinal {expected.expected_recommended_collision_ordinal}, "
            f"got {recommended.ordinal}"
        )
    if recommended.pair != expected.expected_recommended_pair:
        raise RuntimeError(
            "frozen E4 recommended pair drifted: "
            f"expected {expected.expected_recommended_pair}, got {recommended.pair}"
        )
    tolerance = max(expected.recipe_tolerance, _PORTABLE_EVENT_LOCATOR_TOLERANCE)
    if abs(recommended.time - expected.expected_recommended_time) > tolerance:
        raise RuntimeError(
            "frozen E4 recommended time drifted: "
            f"expected {expected.expected_recommended_time}, got {recommended.time}, "
            f"tolerance {tolerance}"
        )
    ordinals = tuple(candidate.event.ordinal for candidate in candidates)
    if ordinals != protocol.ranking.expected_shortlist_ordinals:
        raise RuntimeError(
            "frozen E4 shortlist drifted: "
            f"expected {protocol.ranking.expected_shortlist_ordinals}, got {ordinals}"
        )


def _target_change_metrics(
    protocol: MolecularTimeMachineE4Protocol,
    timeline: TimelineRun,
    target: CausalTarget,
    edited_terminal: DiskState,
) -> TargetChangeMetrics:
    positions_by_id = {
        particle_id: position
        for particle_id, position in zip(
            edited_terminal.particle_ids,
            edited_terminal.positions,
            strict=True,
        )
    }
    target_ejected = tuple(
        particle_id
        for particle_id in target.particle_ids
        if not _inside_bounds(positions_by_id[particle_id], target.x_bounds, target.y_bounds)
    )
    collateral_ejected = tuple(
        particle_id
        for particle_id in target.collateral_foreground_particle_ids
        if not protocol.e1_protocol.pattern.contains(positions_by_id[particle_id])
    )
    collateral_fraction = len(collateral_ejected) / len(target.collateral_foreground_particle_ids)
    return TargetChangeMetrics(
        target_ejection_fraction=len(target_ejected) / len(target.particle_ids),
        collateral_ejection_fraction=collateral_fraction,
        target_to_collateral_ratio=(
            len(target_ejected) / len(target.particle_ids) / collateral_fraction
            if collateral_fraction > 0
            else float("inf")
        ),
        target_ejected_particle_ids=target_ejected,
        collateral_ejected_particle_ids=collateral_ejected,
    )


def _select_angle_for_recommended_collision(
    palette: tuple[PalettePreview, ...],
    recommended_event_id: str,
) -> PalettePreview:
    choices = tuple(
        item for item in palette if item.candidate.event.event_id == recommended_event_id
    )
    if not choices:
        raise RuntimeError("E4 recommended collision has no exact previews")
    return min(
        choices,
        key=lambda item: (
            -item.target_metrics.steering_score,
            -item.target_metrics.target_ejection_fraction,
            abs(item.angle_degrees),
            item.angle_degrees,
        ),
    )


def _inside_bounds(
    position: tuple[float, float],
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
) -> bool:
    return x_bounds[0] <= position[0] <= x_bounds[1] and y_bounds[0] <= position[1] <= y_bounds[1]


def _harmonic_mean(left: float, right: float) -> float:
    return 2.0 * left * right / (left + right) if left + right else 0.0
