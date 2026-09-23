"""
pytest data/app_data/00-python/03-lists/04-searching-counting/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
index_or_minus_one = _module.index_or_minus_one
all_indices = _module.all_indices
contains_all = _module.contains_all
contains_same_object = _module.contains_same_object


def test_absent_value_handling():
    assert index_or_minus_one([1, 2, 3], 99) == -1
    assert index_or_minus_one([], 1) == -1
    assert index_or_minus_one([1, 2, 3], 2) == 1


def test_all_indices_completeness_and_order():
    assert all_indices([5, 3, 5, 7], 5) == [0, 2]
    assert all_indices([1, 1, 1], 1) == [0, 1, 2]
    assert all_indices([1, 2, 3], 99) == []


def test_cross_type_equality():
    assert index_or_minus_one([1.0, 2.0], 1) == 0
    assert contains_all([1.0], [1]) is True


def test_contains_all_duplicates_and_empty_needles():
    assert contains_all([1], [1, 1]) is True
    assert contains_all([1, 2], []) is True
    assert contains_all([1, 2], [1, 3]) is False


def test_contains_same_object_distinguishes_equal_from_identical():
    a = [1]
    assert contains_same_object([[1], a], a) is True
    assert contains_same_object([[1]], a) is False
