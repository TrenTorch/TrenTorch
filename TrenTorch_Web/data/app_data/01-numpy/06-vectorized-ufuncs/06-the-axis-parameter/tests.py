"""
pytest data/app_data/01-numpy/06-vectorized-ufuncs/06-the-axis-parameter/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/06-vectorized-ufuncs/{Path(__file__).resolve().parent.name}")
sum_along_axis = _module.sum_along_axis
mean_keeping_dims = _module.mean_keeping_dims
column_maxes = _module.column_maxes
row_argmins = _module.row_argmins


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
