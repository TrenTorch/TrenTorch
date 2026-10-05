"""Contract tests for Gram Matrix."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([[1., 2.], [3., 4.]]), [[10., 14.], [14., 20.]])
    np.testing.assert_allclose(solve([[1.], [2.], [3.]]), [[14.]])
def test_symmetry_and_diagonal():
    result = solve([[1., 0.], [0., 2.], [1., 1.]])
    np.testing.assert_allclose(result, result.T)
    np.testing.assert_allclose(np.diag(result), [2., 5.])
def test_zero_matrix():
    np.testing.assert_array_equal(solve([[0., 0.], [0., 0.]]), np.zeros((2, 2)))
