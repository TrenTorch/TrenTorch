"""
pytest tests.py
"""

import math

from _load import load_solution

_module = load_solution(__file__)
lower_bound = _module.lower_bound
upper_bound = _module.upper_bound
range_query = _module.range_query
insert_sorted = _module.insert_sorted


class _Counting:
    """A number that counts how many times it has been compared."""

    calls = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        _Counting.calls += 1
        return self.value < other.value

    def __le__(self, other):
        _Counting.calls += 1
        return self.value <= other.value

    def __gt__(self, other):
        _Counting.calls += 1
        return self.value > other.value

    def __ge__(self, other):
        _Counting.calls += 1
        return self.value >= other.value


def _brute_lower(a, x):
    return sum(1 for v in a if v < x)


def _brute_upper(a, x):
    return sum(1 for v in a if v <= x)


# ---- 1-7: bounds ----


def test_1_lower_bound_hand_computed():
    a = [1, 3, 3, 3, 7, 9]
    assert lower_bound(a, 3) == 1 and lower_bound(a, 4) == 4 and lower_bound(a, 0) == 0


def test_2_upper_bound_hand_computed():
    a = [1, 3, 3, 3, 7, 9]
    assert upper_bound(a, 3) == 4 and upper_bound(a, 9) == 6 and upper_bound(a, 0) == 0


def test_3_values_beyond_the_ends():
    a = [2, 4, 6]
    assert lower_bound(a, 100) == 3 and upper_bound(a, 100) == 3
    assert lower_bound(a, -5) == 0 and upper_bound(a, -5) == 0


def test_4_empty_and_single_element_lists():
    assert lower_bound([], 5) == 0 and upper_bound([], 5) == 0
    assert lower_bound([5], 5) == 0 and upper_bound([5], 5) == 1


def test_5_both_bounds_match_brute_force_on_many_lists():
    for n in range(0, 12):
        a = sorted([(i * 7) % 5 for i in range(n)])
        for x in range(-1, 7):
            assert lower_bound(a, x) == _brute_lower(a, x)
            assert upper_bound(a, x) == _brute_upper(a, x)


def test_6_difference_counts_the_equal_values():
    a = [1, 2, 2, 2, 2, 5]
    assert upper_bound(a, 2) - lower_bound(a, 2) == 4


def test_7_works_with_floats_and_strings():
    assert lower_bound([0.5, 1.5, 2.5], 1.5) == 1
    assert upper_bound(["a", "c", "c", "e"], "c") == 3


# ---- 8-12: ranges ----


def test_8_range_query_inclusive_on_both_ends():
    assert range_query([1, 3, 5, 7, 9], 3, 7) == [3, 5, 7]


def test_9_range_with_duplicates():
    assert range_query([1, 2, 2, 2, 3, 4], 2, 3) == [2, 2, 2, 3]


def test_10_empty_and_reversed_ranges():
    assert range_query([1, 2, 3], 10, 20) == []
    assert range_query([1, 2, 3], 3, 1) == []
    assert range_query([], 0, 5) == []


def test_11_range_between_stored_values():
    assert range_query([10, 20, 30, 40], 15, 35) == [20, 30]


def test_12_range_covering_everything():
    a = [1, 2, 3]
    assert range_query(a, -100, 100) == [1, 2, 3]


# ---- 13-16: insertion ----


def test_13_insert_keeps_the_list_sorted():
    assert insert_sorted([1, 3, 5], 4) == [1, 3, 4, 5]
    assert insert_sorted([1, 3, 5], 0) == [0, 1, 3, 5]
    assert insert_sorted([1, 3, 5], 9) == [1, 3, 5, 9]


def test_14_equal_values_go_after_existing_ones():
    result = insert_sorted([(1), 2, 2], 2)
    assert result == [1, 2, 2, 2]


def test_15_insertion_does_not_modify_the_input_list():
    a = [1, 2, 3]
    insert_sorted(a, 2)
    assert a == [1, 2, 3]


def test_16_building_a_sorted_list_by_repeated_insertion():
    a = []
    for v in [5, 1, 4, 1, 3]:
        a = insert_sorted(a, v)
    assert a == [1, 1, 3, 4, 5]


# ---- 17-18: it really is logarithmic ----


def test_17_lower_bound_uses_logarithmically_many_comparisons():
    n = 100_000
    a = [_Counting(i) for i in range(n)]
    _Counting.calls = 0
    lower_bound(a, _Counting(54_321))
    assert _Counting.calls <= math.ceil(math.log2(n)) + 2


def test_18_upper_bound_uses_logarithmically_many_comparisons():
    n = 100_000
    a = [_Counting(i) for i in range(n)]
    _Counting.calls = 0
    upper_bound(a, _Counting(77_777))
    assert _Counting.calls <= math.ceil(math.log2(n)) + 2
