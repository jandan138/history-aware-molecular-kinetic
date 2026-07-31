"""Compact exact-history features used by the Phase-I paper story."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from itertools import pairwise

from historykinetic.contracts import CollisionEvent
from historykinetic.graphs.features import summarize_collision_graph
from historykinetic.solvers.result import GeometryCollisionEvent


def summarize_history_window(
    events: Iterable[CollisionEvent],
    *,
    block_id: str,
    window_start: float,
    window_end: float,
    geometry_events: Iterable[GeometryCollisionEvent] = (),
    particle_ids: set[int] | None = None,
) -> dict[str, float]:
    selected = sorted(
        (
            event
            for event in events
            if (
                (
                    event.block_id == block_id
                    if particle_ids is None
                    else event.particle_a in particle_ids
                    or event.particle_b in particle_ids
                )
                and window_start <= event.time <= window_end
            )
        ),
        key=lambda event: event.time,
    )
    graph = summarize_collision_graph(selected)
    lineage_depth: dict[int, int] = {}
    pair_times: dict[tuple[int, int], list[float]] = defaultdict(list)
    pair_correlation_sum = 0.0

    for event in selected:
        next_depth = max(
            lineage_depth.get(event.particle_a, 0),
            lineage_depth.get(event.particle_b, 0),
        ) + 1
        lineage_depth[event.particle_a] = next_depth
        lineage_depth[event.particle_b] = next_depth
        pair_times[event.ordered_pair].append(event.time)
        va = event.pre_velocity_a
        vb = event.pre_velocity_b
        dot = va[0] * vb[0] + va[1] * vb[1]
        scale = 0.5 * (
            va[0] * va[0]
            + va[1] * va[1]
            + vb[0] * vb[0]
            + vb[1] * vb[1]
        )
        pair_correlation_sum += abs(dot) / max(scale, 1.0e-30)

    reencounter_intervals = [
        later - earlier
        for times in pair_times.values()
        for earlier, later in pairwise(times)
    ]
    duration = max(window_end - window_start, 1.0e-30)
    vertex_scale = max(graph.vertex_count, 1)
    selected_geometry = sorted(
        (
            geometry_event
            for geometry_event in geometry_events
            if (
                (
                    geometry_event.block_id == block_id
                    if particle_ids is None
                    else geometry_event.particle_id in particle_ids
                )
                and window_start <= geometry_event.time <= window_end
            )
        ),
        key=lambda geometry_event: geometry_event.time,
    )
    surface_times: dict[tuple[int, str], list[float]] = defaultdict(list)
    for geometry_event in selected_geometry:
        surface_times[(geometry_event.particle_id, geometry_event.surface_id)].append(
            geometry_event.time
        )
    surface_repeats = sum(max(0, len(times) - 1) for times in surface_times.values())
    surface_intervals = [
        later - earlier
        for times in surface_times.values()
        for earlier, later in pairwise(times)
    ]
    unique_geometry_particles = {
        geometry_event.particle_id for geometry_event in selected_geometry
    }
    obstacle_collisions = sum(
        not geometry_event.surface_id.startswith("wall-")
        for geometry_event in selected_geometry
    )
    return {
        "history_collision_rate": graph.collision_count / duration,
        "history_unique_pair_fraction": graph.unique_pair_count
        / max(graph.collision_count, 1),
        "history_repeated_pair_ratio": graph.repeated_pair_ratio,
        "history_vertex_count": float(graph.vertex_count),
        "history_component_count": float(graph.component_count),
        "history_cycle_rank": float(graph.cycle_rank),
        "history_cycle_rank_per_vertex": graph.cycle_rank / vertex_scale,
        "history_largest_component_fraction": graph.largest_component_fraction,
        "history_mean_lineage_depth": (
            sum(lineage_depth.values()) / len(lineage_depth) if lineage_depth else 0.0
        ),
        "history_pair_velocity_correlation": (
            pair_correlation_sum / len(selected) if selected else 0.0
        ),
        "history_mean_reencounter_time": (
            sum(reencounter_intervals) / len(reencounter_intervals)
            if reencounter_intervals
            else duration
        ),
        "history_geometry_collision_rate": len(selected_geometry) / duration,
        "history_geometry_unique_particles": float(len(unique_geometry_particles)),
        "history_surface_repeat_ratio": surface_repeats
        / max(len(selected_geometry), 1),
        "history_obstacle_collision_fraction": obstacle_collisions
        / max(len(selected_geometry), 1),
        "history_mean_surface_reencounter_time": (
            sum(surface_intervals) / len(surface_intervals)
            if surface_intervals
            else duration
        ),
    }
