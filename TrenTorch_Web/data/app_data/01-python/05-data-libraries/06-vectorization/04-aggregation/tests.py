"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
compute_summary = _module.compute_summary
sum_with_loop = _module.sum_with_loop
sum_along_axis = _module.sum_along_axis
mean_keeping_dims = _module.mean_keeping_dims
column_maxes = _module.column_maxes
row_argmins = _module.row_argmins


def test_compute_summary_correctness_for_all_seven_keys():
    arr = np.array([4, 8, 15, 16, 23, 42])
    result = compute_summary(arr)
    assert result["sum"] == 108
    assert result["mean"] == 18.0
    assert result["min"] == 4
    assert result["max"] == 42
    assert result["argmin"] == 0
    assert result["argmax"] == 5
    np.testing.assert_allclose(result["std"], arr.std())


def test_argmin_argmax_correctness_with_duplicate_extreme_values():
    arr = np.array([5, 1, 3, 1, 5])
    result = compute_summary(arr)
    assert result["argmin"] == 1
    assert result["argmax"] == 0


def test_sum_with_loop_matches_arr_sum():
    arr = np.array([-3, 5, 2, -8, 10])
    assert sum_with_loop(arr) == arr.sum()

    float_arr = np.array([1.5, 2.5, -3.25])
    np.testing.assert_allclose(sum_with_loop(float_arr), float_arr.sum())


def test_single_element_array_edge_case():
    arr = np.array([7])
    result = compute_summary(arr)
    assert result["sum"] == 7
    assert result["mean"] == 7
    assert result["min"] == 7
    assert result["max"] == 7
    assert result["argmin"] == 0
    assert result["argmax"] == 0


def test_sum_along_axis_correctness_for_both_axes_of_2d_array():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    result0 = sum_along_axis(arr, 0)
    np.testing.assert_array_equal(result0, [5, 7, 9])
    assert result0.shape == (3,)

    result1 = sum_along_axis(arr, 1)
    np.testing.assert_array_equal(result1, [6, 15])
    assert result1.shape == (2,)


def test_mean_keeping_dims_correct_shape():
    arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    result = mean_keeping_dims(arr, 1)
    assert result.shape == (2, 1)
    assert result.ndim == 2
    np.testing.assert_allclose(result, [[2.0], [5.0]])


def test_column_maxes_correctness():
    matrix = np.array([[1, 9, 3], [7, 2, 8]])
    result = column_maxes(matrix)
    np.testing.assert_array_equal(result, [7, 9, 8])


def test_row_argmins_correctness():
    matrix = np.array([[5, 1, 3], [4, 6, 2]])
    result = row_argmins(matrix)
    np.testing.assert_array_equal(result, [1, 2])


def test_3d_array_axis_handling():
    arr = np.arange(24).reshape(2, 3, 4)
    result = sum_along_axis(arr, 1)
    assert result.shape == (2, 4)
