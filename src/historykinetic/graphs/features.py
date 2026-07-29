from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass

from historykinetic.contracts import CollisionEvent


@dataclass(frozen=True, slots=True)
class CollisionGraphSummary:
    collision_count: int
    unique_pair_count: int
    repeated_pair_ratio: float
    vertex_count: int
    component_count: int
    cycle_rank: int
    largest_component_fraction: float


class _DisjointSet:
    def __init__(self) -> None:
        self.parent: dict[int, int] = {}
        self.size: dict[int, int] = {}

    def add(self, item: int) -> None:
        if item not in self.parent:
            self.parent[item] = item
            self.size[item] = 1

    def find(self, item: int) -> int:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != item:
            parent = self.parent[item]
            self.parent[item] = root
            item = parent
        return root

    def union(self, left: int, right: int) -> None:
        self.add(left)
        self.add(right)
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return
        if self.size[root_left] < self.size[root_right]:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        self.size[root_left] += self.size[root_right]


def summarize_collision_graph(events: Iterable[CollisionEvent]) -> CollisionGraphSummary:
    materialized = list(events)
    if not materialized:
        return CollisionGraphSummary(0, 0, 0.0, 0, 0, 0, 0.0)

    pair_counts = Counter(event.ordered_pair for event in materialized)
    repeated_events = sum(count - 1 for count in pair_counts.values() if count > 1)

    dsu = _DisjointSet()
    for event in materialized:
        dsu.union(event.particle_a, event.particle_b)

    roots = {dsu.find(vertex) for vertex in dsu.parent}
    component_sizes = Counter(dsu.find(vertex) for vertex in dsu.parent)
    vertex_count = len(dsu.parent)
    component_count = len(roots)
    unique_pair_count = len(pair_counts)
    cycle_rank = max(0, unique_pair_count - vertex_count + component_count)
    largest_fraction = max(component_sizes.values()) / vertex_count if vertex_count else 0.0

    return CollisionGraphSummary(
        collision_count=len(materialized),
        unique_pair_count=unique_pair_count,
        repeated_pair_ratio=repeated_events / len(materialized),
        vertex_count=vertex_count,
        component_count=component_count,
        cycle_rank=cycle_rank,
        largest_component_fraction=largest_fraction,
    )
