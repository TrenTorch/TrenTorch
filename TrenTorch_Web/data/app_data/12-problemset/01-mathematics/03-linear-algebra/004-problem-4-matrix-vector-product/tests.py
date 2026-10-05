"""Contract tests for Matrix-Vector Product."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([[1., 2.], [3., 4.]], [1., 2.]), [5., 11.])
    np.testing.assert_allclose(solve([[2., -1.]], [3., 4.]), [2.])
def test_rectangular_matrix():
    np.testing.assert_allclose(solve([[1., 0., 2.], [-1., 3., 1.]], [2., 1., 4.]), [10., 5.])
def test_zero_vector():
    np.testing.assert_allclose(solve([[2., 1.], [0., -3.]], [0., 0.]), [0., 0.])
