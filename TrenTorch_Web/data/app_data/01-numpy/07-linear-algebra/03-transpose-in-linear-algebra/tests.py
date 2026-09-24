"""
pytest data/app_data/01-numpy/07-linear-algebra/03-transpose-in-linear-algebra/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/07-linear-algebra/{Path(__file__).resolve().parent.name}")
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
