"""
pytest data/app_data/00-python/05-dictionaries/06-dict-comprehensions/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/05-dictionaries/{Path(__file__).resolve().parent.name}")
square_map = _module.square_map
invert = _module.invert
filter_items = _module.filter_items
dict_from_parallel = _module.dict_from_parallel


def test_square_map_bounds():
    assert square_map(1) == {1: 1}
    assert square_map(0) == {}
    assert square_map(-5) == {}
    assert square_map(5) == {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}


def test_invert_collision_rule():
    d = {"a": 1, "b": 1, "c": 2}
    result = invert(d)
    assert result == {1: "b", 2: "c"}
    assert len(result) < len(d)


def test_invert_and_filter_items_do_not_mutate_input():
    d = {"a": 1, "b": 2}
    invert(d)
    filter_items(d, 1)
    assert d == {"a": 1, "b": 2}
    result = filter_items(d, 1)
    assert id(result) != id(d)


def test_filter_items_boundary():
    d = {"a": 1, "b": 2, "c": 3}
    assert filter_items(d, 2) == {"b": 2, "c": 3}


def test_dict_from_parallel_unequal_lengths():
    assert dict_from_parallel(["a", "b", "c"], [1, 2]) == {"a": 1, "b": 2}
    assert dict_from_parallel(["a"], [1, 2, 3]) == {"a": 1}
    assert dict_from_parallel([], []) == {}
