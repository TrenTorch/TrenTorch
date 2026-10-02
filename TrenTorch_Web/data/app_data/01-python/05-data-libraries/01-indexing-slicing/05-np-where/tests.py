"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
find_indices_above = _module.find_indices_above
replace_above_threshold = _module.replace_above_threshold
sign_labels = _module.sign_labels


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
