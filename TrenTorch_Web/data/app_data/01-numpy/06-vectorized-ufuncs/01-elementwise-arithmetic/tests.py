"""
pytest data/app_data/01-numpy/06-vectorized-ufuncs/01-elementwise-arithmetic/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/06-vectorized-ufuncs/{Path(__file__).resolve().parent.name}")
elementwise_multiply = _module.elementwise_multiply
increment_in_place = _module.increment_in_place
square_each = _module.square_each


def test_elementwise_multiply_correctness():
    a = np.array([1, 2, 3])
    b = np.array([10, 20, 30])
    np.testing.assert_array_equal(elementwise_multiply(a, b), [10, 40, 90])


def test_increment_in_place_mutates_correct_buffer():
    arr = np.array([1, 2, 3])
    original_id = id(arr)
    increment_in_place(arr, 5)
    assert id(arr) == original_id
    np.testing.assert_array_equal(arr, [6, 7, 8])


def test_square_each_does_not_mutate_input():
    arr = np.array([1, 2, 3])
    result = square_each(arr)
    np.testing.assert_array_equal(result, [1, 4, 9])
    np.testing.assert_array_equal(arr, [1, 2, 3])
    assert not np.shares_memory(arr, result)


def test_2d_array_support():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    np.testing.assert_array_equal(elementwise_multiply(a, b), [[5, 12], [21, 32]])
    np.testing.assert_array_equal(square_each(a), [[1, 4], [9, 16]])
    increment_in_place(a, 1)
    np.testing.assert_array_equal(a, [[2, 3], [4, 5]])
