"""
pytest tests.py
"""

import math
import random

from _load import load_solution

_module = load_solution(__file__)
running_sum = _module.running_sum
rank = _module.rank
lag = _module.lag
moving_average = _module.moving_average


# ---- 1-5: running sum ----


def test_1_running_sum_without_partitions():
    assert running_sum([1, 2, 3, 4], ["a"] * 4) == [1, 3, 6, 10]


def test_2_running_sum_restarts_in_each_partition():
    values = [10, 1, 20, 2, 30]
    partitions = ["x", "y", "x", "y", "x"]
    assert running_sum(values, partitions) == [10, 1, 30, 3, 60]


def test_3_running_sum_matches_a_brute_force_computation():
    rng = random.Random(0)
    values = [rng.randint(-5, 5) for _ in range(50)]
    partitions = [rng.randint(0, 3) for _ in range(50)]
    expected = [
        sum(values[j] for j in range(i + 1) if partitions[j] == partitions[i]) for i in range(50)
    ]
    assert running_sum(values, partitions) == expected


def test_4_running_sum_of_floats_and_empty_input():
    assert running_sum([0.5, 0.25], [1, 1]) == [0.5, 0.75]
    assert running_sum([], []) == []


def test_5_inputs_are_not_modified():
    values, partitions = [1, 2, 3], ["a", "b", "a"]
    running_sum(values, partitions)
    rank(values, partitions)
    lag(values, partitions, 1)
    moving_average(values, 2)
    assert values == [1, 2, 3] and partitions == ["a", "b", "a"]


# ---- 6-10: rank ----


def test_6_rank_highest_value_is_one():
    assert rank([30, 10, 20], ["a", "a", "a"]) == [1, 3, 2]


def test_7_ties_share_a_rank_and_the_next_is_skipped():
    assert rank([9, 9, 7], ["a", "a", "a"]) == [1, 1, 3]
    assert rank([5, 5, 5], ["a", "a", "a"]) == [1, 1, 1]


def test_8_rank_is_computed_within_each_partition():
    values = [100, 5, 50, 7]
    partitions = ["x", "y", "x", "y"]
    assert rank(values, partitions) == [1, 2, 2, 1]


def test_9_rank_depends_on_all_rows_in_the_partition_not_only_earlier_ones():
    assert rank([1, 2, 3], ["a", "a", "a"]) == [3, 2, 1]


def test_10_rank_single_row_partitions():
    assert rank([4, 8, 6], ["a", "b", "c"]) == [1, 1, 1]


# ---- 11-15: lag ----


def test_11_lag_one_within_a_single_partition():
    assert lag([1, 2, 3, 4], ["a"] * 4, 1) == [None, 1, 2, 3]


def test_12_lag_uses_the_default_when_there_is_no_earlier_row():
    assert lag([1, 2, 3], ["a"] * 3, 2, default=-1) == [-1, -1, 1]


def test_13_lag_looks_only_inside_the_partition():
    values = [10, 1, 20, 2, 30]
    partitions = ["x", "y", "x", "y", "x"]
    assert lag(values, partitions, 1, default=0) == [0, 0, 10, 1, 20]


def test_14_lag_matches_a_brute_force_computation():
    rng = random.Random(1)
    values = [rng.randint(0, 99) for _ in range(60)]
    partitions = [rng.randint(0, 2) for _ in range(60)]
    got = lag(values, partitions, 2, default=None)
    for i in range(60):
        earlier = [values[j] for j in range(i) if partitions[j] == partitions[i]]
        assert got[i] == (earlier[-2] if len(earlier) >= 2 else None)


def test_15_difference_from_the_previous_value_is_a_lag_feature():
    values = [5, 8, 6, 9]
    previous = lag(values, ["s"] * 4, 1, default=0)
    assert [v - p for v, p in zip(values, previous)] == [5, 3, -2, 3]


# ---- 16-19: moving average ----


def test_16_moving_average_hand_computed():
    assert moving_average([2, 4, 6, 8], 2) == [2.0, 3.0, 5.0, 7.0]


def test_17_early_entries_average_over_fewer_values():
    assert moving_average([3, 5, 10], 3) == [3.0, 4.0, 6.0]


def test_18_window_of_one_is_the_values_themselves_and_returns_floats():
    out = moving_average([1, 2, 3], 1)
    assert out == [1.0, 2.0, 3.0] and all(isinstance(v, float) for v in out)


def test_19_a_wide_window_gives_the_running_mean():
    values = [1, 2, 3, 4, 5]
    out = moving_average(values, 100)
    expected = [sum(values[: i + 1]) / (i + 1) for i in range(5)]
    assert all(math.isclose(a, b) for a, b in zip(out, expected))
