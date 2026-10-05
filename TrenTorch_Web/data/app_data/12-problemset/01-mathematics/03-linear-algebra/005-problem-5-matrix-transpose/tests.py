"""Contract tests for Matrix Transpose."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_array_equal(solve([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])
    np.testing.assert_array_equal(solve([[7, 8]]), [[7], [8]])
def test_transpose_round_trip():
    matrix = np.array([[2., 3.], [5., 7.], [11., 13.]])
    np.testing.assert_array_equal(solve(solve(matrix)), matrix)
def test_square_matrix():
    np.testing.assert_array_equal(solve([[1, 2], [3, 4]]), [[1, 3], [2, 4]])
