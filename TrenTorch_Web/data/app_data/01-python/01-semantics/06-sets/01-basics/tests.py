"""
pytest tests.py
"""

import pytest
from _load import load_solution

_module = load_solution(__file__)
unique_values = _module.unique_values
contains_all = _module.contains_all
unique_count = _module.unique_count
add_values = _module.add_values
remove_if_present = _module.remove_if_present
remove_required = _module.remove_required
empty_set = _module.empty_set


def test_duplicate_removal():
    assert unique_values([1, 2, 2, 3, 1]) == {1, 2, 3}


def test_empty_input():
    assert unique_values([]) == set()
    assert unique_count([]) == 0


def test_membership():
    assert contains_all([1, 2, 3, 4], [2, 4]) is True
    assert contains_all([1, 2, 3], [2, 5]) is False
    assert contains_all([1, 2, 3], []) is True


def test_hashable_values():
    assert unique_values(["a", "b", "a"]) == {"a", "b"}
    assert unique_values([(1, 2), (1, 2), (3, 4)]) == {(1, 2), (3, 4)}


def test_no_positional_assumptions():
    assert unique_count([3, 1, 2, 1, 3, 3]) == 3
    assert unique_values([3, 1, 2, 1, 3, 3]) == {1, 2, 3}


def test_add_uniqueness():
    original = {1, 2}
    result = add_values(original, [2, 3, 4])
    assert result == {1, 2, 3, 4}
    assert original == {1, 2}


def test_discard_absent_value():
    s = {1, 2, 3}
    result = remove_if_present(s, 99)
    assert result == {1, 2, 3}


def test_remove_absent_value_raises():
    s = {1, 2}
    with pytest.raises(KeyError):
        remove_required(s, 99)


def test_mutation_and_identity():
    s = {1, 2, 3}
    result = remove_if_present(s, 2)
    assert result is s
    assert s == {1, 3}

    s2 = {1, 2, 3}
    result2 = remove_required(s2, 2)
    assert result2 is s2


def test_clear():
    s = {1, 2, 3}
    result = empty_set(s)
    assert result == set()
    assert result is s
