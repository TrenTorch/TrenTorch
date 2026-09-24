"""
pytest data/app_data/01-numpy/05-broadcasting/03-compatible-shape-examples/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/05-broadcasting/{Path(__file__).resolve().parent.name}")
add_scalar = _module.add_scalar
add_row_vector = _module.add_row_vector
add_column_vector = _module.add_column_vector
outer_sum = _module.outer_sum


def test_add_scalar_correctness():
    matrix = np.ones((2, 3))
    np.testing.assert_array_equal(add_scalar(matrix, 5), np.full((2, 3), 6.0))


def test_add_row_vector_correctness():
    matrix = np.ones((2, 3))
    row = np.array([1, 2, 3])
    np.testing.assert_array_equal(add_row_vector(matrix, row), [[2, 3, 4], [2, 3, 4]])


def test_add_column_vector_correctness():
    matrix = np.ones((3, 2))
    col = np.array([10, 20, 30])
    result = add_column_vector(matrix, col)
    np.testing.assert_array_equal(result, [[11, 11], [21, 21], [31, 31]])


def test_add_column_vector_fails_without_reshaping():
    matrix = np.ones((4, 3))
    col = np.array([10, 20, 30, 40])
    try:
        bad = matrix + col
        assert bad.shape != (4, 3) or not np.array_equal(bad, add_column_vector(matrix, col))
    except ValueError:
        pass


def test_outer_sum_correctness_and_shape():
    row_values = np.array([1, 2, 3])
    col_values = np.array([10, 20])
    result = outer_sum(row_values, col_values)
    assert result.shape == (2, 3)
    np.testing.assert_array_equal(result, [[11, 12, 13], [21, 22, 23]])
