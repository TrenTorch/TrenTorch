"""
pytest data/app_data/00-python/05-dictionaries/07-nested-dictionaries/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/05-dictionaries/{Path(__file__).resolve().parent.name}")
nested_get = _module.nested_get
nested_set = _module.nested_set
flatten_two_levels = _module.flatten_two_levels


def test_nested_get_missing_levels_and_non_dict_intermediates():
    d = {"a": {"b": 1}}
    assert nested_get(d, ["z", "b"], 0) == 0
    assert nested_get(d, ["a", "z"], 0) == 0
    assert nested_get({"a": 5}, ["a", "b"], 0) == 0
    assert nested_get(d, ["a", "b"], 0) == 1
    assert nested_get(d, [], 0) == d


def test_nested_get_does_not_create_keys():
    d = {"a": {"b": 1}}
    nested_get(d, ["a", "z"], 0)
    assert d == {"a": {"b": 1}}


def test_nested_set_creates_intermediates_and_mutates_in_place():
    d = {}
    before_id = id(d)
    nested_set(d, ["a", "b"], 1)
    assert d == {"a": {"b": 1}}
    assert id(d) == before_id
    nested_set(d, ["a", "c"], 2)
    assert d == {"a": {"b": 1, "c": 2}}


def test_nested_set_overwrites_non_dictionary_intermediates():
    d = {"a": 5}
    nested_set(d, ["a", "b"], 1)
    assert d == {"a": {"b": 1}}


def test_flatten_two_levels_order_and_empty_inner():
    result = flatten_two_levels({"a": {"x": 1, "y": 2}, "b": {}, "c": {"x": 3}})
    assert result == {"a.x": 1, "a.y": 2, "c.x": 3}


def test_sibling_independence():
    d = {}
    nested_set(d, ["a", "x"], {})
    nested_set(d, ["b", "x"], {})
    assert id(d["a"]) != id(d["b"])
