"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
index_or_minus_one = _module.index_or_minus_one
all_indices = _module.all_indices
contains_all = _module.contains_all
contains_same_object = _module.contains_same_object
sorted_desc_copy = _module.sorted_desc_copy
sort_in_place_by_length = _module.sort_in_place_by_length
last_char = _module.last_char
sort_by_last_char = _module.sort_by_last_char
reversed_copy = _module.reversed_copy


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
