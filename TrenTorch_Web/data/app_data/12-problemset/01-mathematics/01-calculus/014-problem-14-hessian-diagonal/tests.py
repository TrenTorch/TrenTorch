"""Contract tests for Hessian Diagonal."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve(lambda z: np.sum(z*z), [1., 2.]), [2., 2.], atol=1e-5)
    np.testing.assert_allclose(solve(lambda z: z[0]**2+3*z[1]**2, [0., 1.]), [2., 6.], atol=1e-5)
def test_constant_curvature():
    np.testing.assert_allclose(solve(lambda z: 2*z[0]**2+4*z[1]**2, [3., -1.]), [4., 8.], atol=1e-4)
def test_custom_step():
    np.testing.assert_allclose(solve(lambda z: z[0]**3, [2.], 1e-3), [12.], atol=1e-5)
