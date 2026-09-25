"""
pytest data/app_data/00-python/05-dictionaries/04-iterating-views/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/05-dictionaries/{Path(__file__).resolve().parent.name}")
sum_of_values = _module.sum_of_values
keys_with_max_value = _module.keys_with_max_value
remove_where_value_below = _module.remove_where_value_below
value_of = _module.value_of
items_by_value_desc = _module.items_by_value_desc


def test_sum_of_values_empty_and_negative():
    assert sum_of_values({}) == 0
    assert sum_of_values({"a": -3, "b": 5}) == 2


def test_keys_with_max_value_ties_and_order():
    assert keys_with_max_value({"a": 3, "b": 5, "c": 5}) == ["b", "c"]
    assert keys_with_max_value({"a": 3}) == ["a"]
    assert keys_with_max_value({}) == []


def test_remove_where_value_below_runs_and_mutates():
    d = {"a": 1, "b": 5, "c": 10}
    before_id = id(d)
    remove_where_value_below(d, 5)
    assert d == {"b": 5, "c": 10}
    assert id(d) == before_id


def test_removal_of_adjacent_and_all_entries():
    d = {"a": 1, "b": 2, "c": 3}
    remove_where_value_below(d, 100)
    assert d == {}


def test_items_by_value_desc_order_with_ties():
    d = {"z": 1, "a": 3, "m": 1}
    result = items_by_value_desc(d)
    assert result == [("a", 3), ("m", 1), ("z", 1)]


def test_input_dictionary_unchanged():
    d = {"z": 1, "a": 3}
    items_by_value_desc(d)
    assert d == {"z": 1, "a": 3}
    assert list(d.items()) == [("z", 1), ("a", 3)]
