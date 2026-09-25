"""
pytest data/app_data/00-python/06-sets/05-set-use-cases/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/06-sets/{Path(__file__).resolve().parent.name}")
find_duplicates = _module.find_duplicates
unique_in_first_seen_order = _module.unique_in_first_seen_order
all_seen_before = _module.all_seen_before
missing_values = _module.missing_values


def test_duplicate_detection():
    assert find_duplicates([1, 2, 1, 3, 2, 2]) == {1, 2}


def test_first_seen_order():
    assert unique_in_first_seen_order([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_no_duplicates():
    assert find_duplicates([1, 2, 3]) == set()
    assert unique_in_first_seen_order([1, 2, 3]) == [1, 2, 3]


def test_repeated_values():
    assert find_duplicates([5, 5, 5, 5]) == {5}
    assert all_seen_before([1, 2, 1, 2]) is True
    assert all_seen_before([1, 2, 1]) is False


def test_missing_values():
    assert missing_values([1, 3, 3], {1, 2, 3, 4}) == {2, 4}
    assert missing_values([], {1, 2}) == {1, 2}
    assert missing_values([1, 2], {1, 2}) == set()


def test_input_preservation():
    values = [1, 2, 1, 3]
    expected = {1, 2, 3, 4}
    find_duplicates(values)
    unique_in_first_seen_order(values)
    missing_values(values, expected)
    assert values == [1, 2, 1, 3]
    assert expected == {1, 2, 3, 4}
