"""
pytest tests.py
"""

import numpy as np
import pytest
from _load import load_solution

_module = load_solution(__file__)
reshape_to = _module.reshape_to
reshape_with_inferred_dim = _module.reshape_with_inferred_dim
reshape_shares_memory = _module.reshape_shares_memory
flatten_safe = _module.flatten_safe
flatten_efficient = _module.flatten_efficient
compare_flatten_ravel = _module.compare_flatten_ravel


def test_reshape_to_correctness_across_dimensions():
    arr = np.arange(12)
    np.testing.assert_array_equal(reshape_to(arr, (3, 4)), arr.reshape(3, 4))
    np.testing.assert_array_equal(reshape_to(arr, (2, 3, 2)), arr.reshape(2, 3, 2))


def test_reshape_with_inferred_dim_correct_automatic_dimension():
    arr = np.arange(12)
    result = reshape_with_inferred_dim(arr, 4)
    assert result.shape == (3, 4)
    result2 = reshape_with_inferred_dim(arr, 6)
    assert result2.shape == (2, 6)


def test_reshape_raises_on_incompatible_size():
    arr = np.arange(12)
    with pytest.raises(ValueError):
        reshape_to(arr, (3, 5))


def test_reshape_shares_memory_correctly_reports_view_case():
    arr = np.arange(6)
    assert reshape_shares_memory(arr, (2, 3)) is True


def test_values_preserved_in_correct_order_after_reshape():
    arr = np.arange(6)
    result = reshape_to(arr, (2, 3))
    np.testing.assert_array_equal(result[0], [0, 1, 2])
    np.testing.assert_array_equal(result[1], [3, 4, 5])


def test_flatten_safe_correctness_and_independence():
    arr = np.array([[1, 2], [3, 4]])
    result = flatten_safe(arr)
    np.testing.assert_array_equal(result, [1, 2, 3, 4])
    result[0] = 99
    np.testing.assert_array_equal(arr, [[1, 2], [3, 4]])


def test_flatten_efficient_correctness():
    arr = np.array([[1, 2], [3, 4]])
    np.testing.assert_array_equal(flatten_efficient(arr), flatten_safe(arr))


def test_compare_flatten_ravel_reports_flatten_shares_memory_false():
    arr = np.array([[1, 2], [3, 4]])
    result = compare_flatten_ravel(arr)
    assert result["flatten_shares_memory"] is False


def test_compare_flatten_ravel_reports_ravel_shares_memory_true_for_contiguous():
    arr = np.array([[1, 2], [3, 4]])
    result = compare_flatten_ravel(arr)
    assert result["ravel_shares_memory"] is True


def test_3d_input_handled_correctly():
    arr = np.arange(24).reshape(2, 3, 4)
    np.testing.assert_array_equal(flatten_safe(arr), np.arange(24))
    np.testing.assert_array_equal(flatten_efficient(arr), np.arange(24))
