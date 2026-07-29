from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from historykinetic.contracts import CollisionEvent
from historykinetic.graphs.features import CollisionGraphSummary, summarize_collision_graph


class RollingCollisionWindow:
    """Reference implementation for correctness tests, not the GPU data structure."""

    def __init__(self, duration: float) -> None:
        if duration <= 0:
            raise ValueError("duration must be positive")
        self.duration = duration
        self._events: deque[CollisionEvent] = deque()

    def push(self, event: CollisionEvent) -> None:
        if self._events and event.time < self._events[-1].time:
            raise ValueError("events must be pushed in non-decreasing time order")
        self._events.append(event)
        self.expire(event.time)

    def extend(self, events: Iterable[CollisionEvent]) -> None:
        for event in events:
            self.push(event)

    def expire(self, now: float) -> None:
        cutoff = now - self.duration
        while self._events and self._events[0].time < cutoff:
            self._events.popleft()

    def summary(self, now: float | None = None) -> CollisionGraphSummary:
        if now is not None:
            self.expire(now)
        return summarize_collision_graph(self._events)

    def __len__(self) -> int:
        return len(self._events)
