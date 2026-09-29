"""
pytest data/app_data/00-python/03-lists/05-ordering-sort/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
sorted_desc_copy = _module.sorted_desc_copy
sort_in_place_by_length = _module.sort_in_place_by_length
last_char = _module.last_char
sort_by_last_char = _module.sort_by_last_char
reversed_copy = _module.reversed_copy


def test_sorted_desc_copy_leaves_input_untouched():
    lst = [3, 1, 2]
    before_id = id(lst)
    result = sorted_desc_copy(lst)
    assert result == [3, 2, 1]
    assert lst == [3, 1, 2]
    assert id(lst) == before_id
    assert id(result) != before_id


def test_sort_in_place_by_length_mutates_and_returns_none():
    words = ["ccc", "a", "bb"]
    before_id = id(words)
    result = sort_in_place_by_length(words)
    assert words == ["a", "bb", "ccc"]
    assert id(words) == before_id
    assert result is None


def test_stability_with_equal_keys():
    words = ["bb", "aa", "c", "dd"]
    sort_in_place_by_length(words)
    assert words == ["c", "bb", "aa", "dd"]


def test_sort_by_last_char_empty_strings_and_ties():
    words = ["ab", "", "cb", "d"]
    result = sort_by_last_char(words)
    assert result[0] == ""
    assert result[1:3] == ["ab", "cb"]
    assert words == ["ab", "", "cb", "d"]


def test_reversed_copy_independence():
    lst = [1, 2, 3]
    result = reversed_copy(lst)
    assert result == [3, 2, 1]
    assert lst == [1, 2, 3]
    assert id(result) != id(lst)
    assert reversed_copy([]) == []
