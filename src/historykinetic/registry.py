from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def register(self, name: str, item: T) -> None:
        if not name:
            raise ValueError("registry name must not be empty")
        if name in self._items:
            raise KeyError(f"duplicate registry entry: {name}")
        self._items[name] = item

    def get(self, name: str) -> T:
        try:
            return self._items[name]
        except KeyError as exc:
            raise KeyError(f"unknown registry entry: {name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))

    def values(self) -> Iterable[T]:
        return self._items.values()

    def __iter__(self) -> Iterator[str]:
        return iter(self.names())

    def __len__(self) -> int:
        return len(self._items)
