"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
get_independent_slice = _module.get_independent_slice
safe_modify_first_n = _module.safe_modify_first_n


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
