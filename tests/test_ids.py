from historykinetic.ids import canonical_json, content_id


def test_canonical_json_is_order_independent() -> None:
    assert canonical_json({"b": 2, "a": 1}) == canonical_json({"a": 1, "b": 2})


def test_content_id_is_stable() -> None:
    assert content_id("case", {"a": 1}) == content_id("case", {"a": 1})
    assert content_id("case", {"a": 1}) != content_id("case", {"a": 2})
