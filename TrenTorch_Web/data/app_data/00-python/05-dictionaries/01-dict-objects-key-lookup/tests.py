"""
pytest data/app_data/00-python/05-dictionaries/01-dict-objects-key-lookup/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/05-dictionaries/{Path(__file__).resolve().parent.name}")
first_positions = _module.first_positions
same_key = _module.same_key
distinct_key_count = _module.distinct_key_count


def test_first_positions_keeps_first_index():
    assert first_positions(["a", "b", "a"]) == {"a": 0, "b": 1}
    assert first_positions([]) == {}


def test_same_key_numeric_equivalence():
    assert same_key(1, 1.0) is True
    assert same_key(1, True) is True
    assert same_key(1, "1") is False


def test_same_key_tuples():
    assert same_key(tuple([1, 2]), (1, 2)) is True
    assert same_key((1, 2), (1, 3)) is False


def test_distinct_key_count_merges_equal_keys():
    assert distinct_key_count([1, 1.0, True]) == 1
    assert distinct_key_count(["a", "A"]) == 2


def test_input_lists_unchanged():
    words = ["a", "b", "a"]
    keys = [1, 1.0, True]
    first_positions(words)
    distinct_key_count(keys)
    assert words == ["a", "b", "a"]
    assert keys == [1, 1.0, True]
