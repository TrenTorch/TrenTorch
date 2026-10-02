"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
pairwise_row_dots = _module.pairwise_row_dots
matrix_vector_product = _module.matrix_vector_product


def test_pairwise_row_dots_correctness():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    result = pairwise_row_dots(a, b)
    np.testing.assert_array_equal(result, [[17, 23], [39, 53]])


def test_pairwise_row_dots_correct_output_shape():
    a = np.arange(6).reshape(2, 3)
    b = np.arange(12).reshape(4, 3)
    result = pairwise_row_dots(a, b)
    assert result.shape == (2, 4)


def test_matrix_vector_product_correctness():
    matrix = np.array([[1, 2], [3, 4]])
    vector = np.array([5, 6])
    np.testing.assert_array_equal(matrix_vector_product(matrix, vector), [17, 39])


def test_matrix_vector_product_returns_correct_shape():
    matrix = np.arange(12).reshape(3, 4)
    vector = np.array([1, 1, 1, 1])
    result = matrix_vector_product(matrix, vector)
    assert result.shape == (3,)
    assert result.ndim == 1
