"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
square_map = _module.square_map
invert = _module.invert
filter_items = _module.filter_items
dict_from_parallel = _module.dict_from_parallel
nested_get = _module.nested_get
nested_set = _module.nested_set
flatten_two_levels = _module.flatten_two_levels


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
