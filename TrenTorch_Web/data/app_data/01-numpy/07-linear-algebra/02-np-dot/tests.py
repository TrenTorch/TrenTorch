"""
pytest data/app_data/01-numpy/07-linear-algebra/02-np-dot/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/07-linear-algebra/{Path(__file__).resolve().parent.name}")
vector_dot_product = _module.vector_dot_product
matrix_product_via_dot = _module.matrix_product_via_dot


def test_vector_dot_product_correctness():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    assert vector_dot_product(a, b) == 32

    c = np.array([-1, 2, -3])
    d = np.array([4, -5, 6])
    assert vector_dot_product(c, d) == -1 * 4 + 2 * -5 + -3 * 6


def test_vector_dot_product_returns_scalar_not_array():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    result = vector_dot_product(a, b)
    assert np.isscalar(result) or (hasattr(result, "shape") and result.shape == ())


def test_matrix_product_via_dot_matches_at_operator():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    np.testing.assert_array_equal(matrix_product_via_dot(a, b), a @ b)


def test_orthogonal_vectors_produce_zero_dot_product():
    a = np.array([1, 0])
    b = np.array([0, 1])
    assert vector_dot_product(a, b) == 0
