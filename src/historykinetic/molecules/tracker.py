from __future__ import annotations

import random
from collections import Counter

from historykinetic.molecules.models import ComponentView


class MoleculeTracker:
    """Online finite collision-molecule analogue for E2.

    Accepted collisions are multigraph edges on particle identities. Joining two
    components leaves circuit rank unchanged; an edge within one component adds one
    independent cycle. Suppressed overlaps never mutate this tracker.
    """

    def __init__(self, particle_ids: tuple[int, ...]) -> None:
        if not particle_ids or len(set(particle_ids)) != len(particle_ids):
            raise ValueError("molecule tracker requires unique particle IDs")
        self._particle_ids = tuple(sorted(particle_ids))
        self._parent = {particle_id: particle_id for particle_id in self._particle_ids}
        self._members = {
            particle_id: {particle_id} for particle_id in self._particle_ids
        }
        self._cycle_rank = {particle_id: 0 for particle_id in self._particle_ids}
        self._last_collision_event: dict[int, int | None] = {
            particle_id: None for particle_id in self._particle_ids
        }
        self._pair_multiplicity: Counter[tuple[int, int]] = Counter()

    def _find(self, particle_id: int) -> int:
        if particle_id not in self._parent:
            raise KeyError(f"unknown particle ID: {particle_id}")
        root = particle_id
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[particle_id] != particle_id:
            parent = self._parent[particle_id]
            self._parent[particle_id] = root
            particle_id = parent
        return root

    def component(self, particle_id: int) -> ComponentView:
        root = self._find(particle_id)
        return ComponentView(
            component_id=root,
            size=len(self._members[root]),
            cycle_rank=self._cycle_rank[root],
        )

    def predecessors(self, left: int, right: int) -> tuple[int | None, int | None]:
        return (
            self._last_collision_event[left],
            self._last_collision_event[right],
        )

    def next_pair_multiplicity(self, left: int, right: int) -> int:
        pair = (min(left, right), max(left, right))
        self._pair_multiplicity[pair] += 1
        return self._pair_multiplicity[pair]

    def budget_allows(
        self,
        left: int,
        right: int,
        *,
        size: int,
        cycles: int,
    ) -> tuple[bool, str]:
        if size < 1 or cycles < 0:
            raise ValueError("molecule budgets must have size >= 1 and cycles >= 0")
        left_component = self.component(left)
        right_component = self.component(right)
        if left_component.component_id == right_component.component_id:
            if left_component.cycle_rank >= cycles:
                return False, "cycle-rank-budget"
            return True, "within-cycle-rank-budget"
        if left_component.size + right_component.size > size:
            return False, "component-size-budget"
        if left_component.cycle_rank + right_component.cycle_rank > cycles:
            return False, "merged-cycle-rank-budget"
        return True, "within-component-budget"

    def accept_collision(self, left: int, right: int, *, event_id: int) -> ComponentView:
        root_left = self._find(left)
        root_right = self._find(right)
        if root_left == root_right:
            self._cycle_rank[root_left] += 1
            root_after = root_left
        else:
            root_after = min(root_left, root_right)
            root_removed = max(root_left, root_right)
            merged_members = self._members[root_left] | self._members[root_right]
            merged_rank = self._cycle_rank[root_left] + self._cycle_rank[root_right]
            self._members[root_after] = merged_members
            self._cycle_rank[root_after] = merged_rank
            for particle_id in merged_members:
                self._parent[particle_id] = root_after
            del self._members[root_removed]
            del self._cycle_rank[root_removed]
        self._last_collision_event[left] = event_id
        self._last_collision_event[right] = event_id
        return self.component(left)

    def shuffle_membership(self, *, seed: int) -> None:
        """Destroy particle-to-component wiring while preserving size/rank multiset."""

        components = sorted(
            (
                len(members),
                self._cycle_rank[root],
                root,
            )
            for root, members in self._members.items()
        )
        shuffled_particles = list(self._particle_ids)
        random.Random(seed).shuffle(shuffled_particles)
        parent: dict[int, int] = {}
        members_by_root: dict[int, set[int]] = {}
        rank_by_root: dict[int, int] = {}
        cursor = 0
        for size, cycle_rank, _old_root in components:
            members = set(shuffled_particles[cursor : cursor + size])
            cursor += size
            root = min(members)
            members_by_root[root] = members
            rank_by_root[root] = cycle_rank
            for particle_id in members:
                parent[particle_id] = root
        self._parent = parent
        self._members = members_by_root
        self._cycle_rank = rank_by_root

    def component_signature(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            sorted(
                (len(members), self._cycle_rank[root])
                for root, members in self._members.items()
            )
        )
