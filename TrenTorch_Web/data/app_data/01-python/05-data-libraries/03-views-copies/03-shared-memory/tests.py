"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
zero_out_via_view = _module.zero_out_via_view
chained_view_mutation = _module.chained_view_mutation
get_independent_slice = _module.get_independent_slice
safe_modify_first_n = _module.safe_modify_first_n


def test_zero_out_via_view_mutates_correct_range():
    arr = np.arange(10)
    zero_out_via_view(arr, 2, 5)
    np.testing.assert_array_equal(arr, [0, 1, 0, 0, 0, 5, 6, 7, 8, 9])


def test_zero_out_via_view_does_not_reassign_arr():
    arr = np.arange(10)
    original_id = id(arr)
    zero_out_via_view(arr, 2, 5)
    assert id(arr) == original_id


def test_chained_view_mutation_propagates_through_whole_chain():
    arr = np.arange(10)
    result = chained_view_mutation(arr)
    np.testing.assert_array_equal(arr[3:6], [-1, -1, -1])
    np.testing.assert_array_equal(result["view1"][2:5], [-1, -1, -1])
    np.testing.assert_array_equal(result["view2"], [-1, -1, -1])


def test_elements_outside_innermost_view_range_remain_untouched():
    arr = np.arange(10)
    chained_view_mutation(arr)
    np.testing.assert_array_equal(arr[0:3], [0, 1, 2])
    np.testing.assert_array_equal(arr[6:], [6, 7, 8, 9])


def test_get_independent_slice_correctness():
    arr = np.arange(10)
    result = get_independent_slice(arr, 2, 5)
    np.testing.assert_array_equal(result, [2, 3, 4])


def test_get_independent_slice_true_independence():
    arr = np.arange(10)
    result = get_independent_slice(arr, 2, 5)
    result[0] = 99
    np.testing.assert_array_equal(arr, np.arange(10))
    arr[2] = -1
    assert result[0] == 99


def test_safe_modify_first_n_does_not_mutate_input():
    arr = np.arange(6)
    original = arr.copy()
    safe_modify_first_n(arr, 3, 0)
    np.testing.assert_array_equal(arr, original)


def test_safe_modify_first_n_correct_partial_modification():
    arr = np.arange(6)
    result = safe_modify_first_n(arr, 3, 0)
    np.testing.assert_array_equal(result[:3], [0, 0, 0])
    np.testing.assert_array_equal(result[3:], arr[3:])
