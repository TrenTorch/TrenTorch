"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
select_above_threshold = _module.select_above_threshold
select_in_range = _module.select_in_range
zero_out_negatives = _module.zero_out_negatives
find_indices_above = _module.find_indices_above
replace_above_threshold = _module.replace_above_threshold
sign_labels = _module.sign_labels


def test_select_above_threshold_correctness():
    arr = np.array([10, 15, 20, 25, 30])
    result = select_above_threshold(arr, 18)
    np.testing.assert_array_equal(result, [20, 25, 30])
    assert 18 not in select_above_threshold(np.array([18]), 18)


def test_select_in_range_correctness_with_combined_condition():
    arr = np.array([5, 10, 15, 20, 25])
    result = select_in_range(arr, 10, 20)
    np.testing.assert_array_equal(result, [15])


def test_masking_returns_copy_not_view():
    arr = np.array([10, 15, 20, 25, 30])
    result = select_above_threshold(arr, 18)
    result[0] = -1
    np.testing.assert_array_equal(arr, [10, 15, 20, 25, 30])


def test_zero_out_negatives_mutates_in_place():
    arr = np.array([-1, 2, -3, 4])
    original_id = id(arr)
    zero_out_negatives(arr)
    assert id(arr) == original_id
    np.testing.assert_array_equal(arr, [0, 2, 0, 4])


def test_all_true_and_all_false_mask_edge_cases():
    all_above = select_above_threshold(np.array([5, 6, 7]), 0)
    np.testing.assert_array_equal(all_above, [5, 6, 7])
    none_above = select_above_threshold(np.array([5, 6, 7]), 100)
    assert none_above.size == 0


def test_find_indices_above_correctness():
    arr = np.array([5, 12, 3, 18, 7])
    np.testing.assert_array_equal(find_indices_above(arr, 10), [1, 3])
    np.testing.assert_array_equal(find_indices_above(arr, 100), [])


def test_replace_above_threshold_correctness_and_non_mutation():
    arr = np.array([5, 12, 3, 18, 7])
    result = replace_above_threshold(arr, 10, -1)
    np.testing.assert_array_equal(result, [5, -1, 3, -1, 7])
    np.testing.assert_array_equal(arr, [5, 12, 3, 18, 7])


def test_sign_labels_correctness_including_zero():
    arr = np.array([-2, 0, 3])
    result = sign_labels(arr)
    assert list(result) == ["non-positive", "non-positive", "positive"]


def test_2d_input_handling_for_replace_above_threshold():
    arr = np.array([[5, 15], [25, 2]])
    result = replace_above_threshold(arr, 10, 0)
    np.testing.assert_array_equal(result, [[5, 0], [0, 2]])
