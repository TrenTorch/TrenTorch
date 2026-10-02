"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
unique_values = _module.unique_values
contains_all = _module.contains_all
unique_count = _module.unique_count


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
