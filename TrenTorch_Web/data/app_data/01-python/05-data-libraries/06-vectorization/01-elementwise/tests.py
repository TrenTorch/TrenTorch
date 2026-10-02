"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
elementwise_multiply = _module.elementwise_multiply
increment_in_place = _module.increment_in_place
square_each = _module.square_each
sqrt_all = _module.sqrt_all
exponentiate = _module.exponentiate
natural_log = _module.natural_log
absolute_values = _module.absolute_values


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


def test_sqrt_all_correctness():
    arr = np.array([1.0, 4.0, 9.0, 16.0])
    np.testing.assert_allclose(sqrt_all(arr), [1.0, 2.0, 3.0, 4.0])


def test_exponentiate_and_natural_log_are_inverses():
    arr = np.array([0.5, 1.0, 2.0])
    result = natural_log(exponentiate(arr))
    np.testing.assert_allclose(result, arr, atol=1e-10)


def test_absolute_values_correctness_with_negative_and_positive_inputs():
    arr = np.array([-3, 2, -1, 0])
    np.testing.assert_array_equal(absolute_values(arr), [3, 2, 1, 0])


def test_all_functions_preserve_shape():
    arr = np.array([[1.0, 4.0], [9.0, 16.0]])
    assert sqrt_all(arr).shape == (2, 2)
    assert exponentiate(arr).shape == (2, 2)
    assert natural_log(arr).shape == (2, 2)
    assert absolute_values(arr).shape == (2, 2)
