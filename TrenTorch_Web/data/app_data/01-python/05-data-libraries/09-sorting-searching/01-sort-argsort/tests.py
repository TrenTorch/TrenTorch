"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sorted_copy = _module.sorted_copy
sort_order = _module.sort_order
rank_of = _module.rank_of
descending_order = _module.descending_order
sort_rows_by_column = _module.sort_rows_by_column


def test_sorted_copy_is_ascending():
    np.testing.assert_array_equal(sorted_copy(np.array([3, 1, 2])), [1, 2, 3])


def test_sorted_copy_does_not_change_the_input():
    a = np.array([3, 1, 2])
    sorted_copy(a)
    np.testing.assert_array_equal(a, [3, 1, 2])


def test_sort_order_gives_the_indices_that_sort():
    a = np.array([30, 10, 20])
    np.testing.assert_array_equal(sort_order(a), [1, 2, 0])
    np.testing.assert_array_equal(a[sort_order(a)], np.sort(a))


def test_sort_order_is_stable_for_ties():
    a = np.array([2, 1, 2, 1, 2])
    np.testing.assert_array_equal(sort_order(a), [1, 3, 0, 2, 4])


def test_rank_of_simple_case():
    np.testing.assert_array_equal(rank_of(np.array([30, 10, 20])), [2, 0, 1])


def test_rank_of_ties_follow_original_order():
    np.testing.assert_array_equal(rank_of(np.array([5, 5, 1])), [1, 2, 0])


def test_rank_is_a_permutation_and_the_inverse_of_the_order():
    a = np.random.default_rng(0).integers(0, 10, size=30)
    r = rank_of(a)
    assert sorted(r.tolist()) == list(range(30))
    np.testing.assert_array_equal(r[sort_order(a)], np.arange(30))


def test_descending_order_largest_first():
    np.testing.assert_array_equal(descending_order(np.array([10.0, 30.0, 20.0])), [1, 2, 0])


def test_descending_order_keeps_tied_elements_in_original_order():
    a = np.array([5, 9, 5, 9, 1])
    np.testing.assert_array_equal(descending_order(a), [1, 3, 0, 2, 4])


def test_descending_order_handles_negative_values():
    np.testing.assert_array_equal(descending_order(np.array([-1.0, -5.0, 3.0])), [2, 0, 1])


def test_sort_rows_by_column_reorders_whole_rows():
    m = np.array([[3, 30], [1, 10], [2, 20]])
    np.testing.assert_array_equal(sort_rows_by_column(m, 0), [[1, 10], [2, 20], [3, 30]])
    np.testing.assert_array_equal(sort_rows_by_column(m, 1), [[1, 10], [2, 20], [3, 30]])


def test_sort_rows_is_stable_and_leaves_the_input_alone():
    m = np.array([[1, 7], [0, 7], [2, 5]])
    out = sort_rows_by_column(m, 1)
    np.testing.assert_array_equal(out, [[2, 5], [1, 7], [0, 7]])
    np.testing.assert_array_equal(m, [[1, 7], [0, 7], [2, 5]])
