"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
distinct = _module.distinct
value_counts = _module.value_counts
first_positions = _module.first_positions
codes = _module.codes
mode = _module.mode
unique_in_order = _module.unique_in_order

A = np.array([3, 1, 2, 3, 1, 3])


def test_distinct_is_sorted_and_has_no_repeats():
    np.testing.assert_array_equal(distinct(A), [1, 2, 3])


def test_distinct_works_on_text():
    np.testing.assert_array_equal(distinct(np.array(["b", "a", "b"])), ["a", "b"])


def test_value_counts_returns_values_and_counts():
    values, counts = value_counts(A)
    np.testing.assert_array_equal(values, [1, 2, 3])
    np.testing.assert_array_equal(counts, [2, 1, 3])


def test_counts_add_up_to_the_length():
    a = np.random.default_rng(0).integers(0, 7, size=50)
    assert value_counts(a)[1].sum() == 50


def test_first_positions_are_the_first_occurrences():
    np.testing.assert_array_equal(first_positions(A), [1, 2, 0])
    for value, position in zip(distinct(A), first_positions(A)):
        assert A[position] == value and value not in A[:position]


def test_codes_index_into_the_distinct_values():
    np.testing.assert_array_equal(codes(A), [2, 0, 1, 2, 0, 2])


def test_codes_reconstruct_the_original_array():
    a = np.random.default_rng(1).integers(-5, 5, size=40)
    np.testing.assert_array_equal(distinct(a)[codes(a)], a)


def test_mode_is_the_most_frequent_value():
    assert mode(A) == 3


def test_mode_ties_go_to_the_smallest_value():
    assert mode(np.array([5, 2, 5, 2, 9])) == 2
    assert mode(np.array([7, 7, 1, 1])) == 1


def test_unique_in_order_keeps_first_appearance_order():
    np.testing.assert_array_equal(unique_in_order(A), [3, 1, 2])


def test_unique_in_order_on_text_and_on_a_single_value():
    np.testing.assert_array_equal(unique_in_order(np.array(["z", "a", "z", "m", "a"])), ["z", "a", "m"])
    np.testing.assert_array_equal(unique_in_order(np.array([4, 4, 4])), [4])


def test_inputs_are_not_changed():
    a = A.copy()
    for f in (distinct, value_counts, first_positions, codes, mode, unique_in_order):
        f(a)
    np.testing.assert_array_equal(a, A)
