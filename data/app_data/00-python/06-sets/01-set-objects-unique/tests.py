"""
pytest data/app_data/00-python/06-sets/01-set-objects-unique/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/06-sets/{Path(__file__).resolve().parent.name}")
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
