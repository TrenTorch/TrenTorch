"""Contract tests for Gradient of a Quadratic."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([[2., 0.], [0., 4.]], [1., 2.], [1., -1.]), [3., 7.])
    np.testing.assert_allclose(solve([[0., 0.], [0., 0.]], [3., 4.], [2., -2.]), [2., -2.])
def test_symmetric_quadratic():
    np.testing.assert_allclose(solve([[1., 2.], [2., 3.]], [2., -1.], [0., 0.]), [0., 1.])
def test_uses_symmetric_part():
    np.testing.assert_allclose(solve([[1., 4.], [0., 2.]], [2., 3.], [1., 1.]), [9., 11.])
