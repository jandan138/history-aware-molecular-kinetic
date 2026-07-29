import pytest

from historykinetic.registry import Registry


def test_registry_orders_names() -> None:
    registry: Registry[int] = Registry()
    registry.register("b", 2)
    registry.register("a", 1)
    assert registry.names() == ("a", "b")


def test_registry_rejects_duplicates() -> None:
    registry: Registry[int] = Registry()
    registry.register("a", 1)
    with pytest.raises(KeyError):
        registry.register("a", 2)
