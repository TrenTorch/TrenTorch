"""Contract tests for Linear Regression Normal Equation."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([[0.],[1.],[2.]], [1.,3.,5.]), [1.,2.], atol=1e-10)
    np.testing.assert_allclose(solve([[1.,0.],[0.,1.],[1.,1.]], [3.,4.,6.]), [1.,2.,3.], atol=1e-10)
def test_fitted_values_recover_targets():
    X = np.array([[0.],[1.],[2.],[3.]])
    y = np.array([2.,3.,4.,5.])
    beta = solve(X,y)
    np.testing.assert_allclose(beta[0] + X @ beta[1:], y, atol=1e-10)
def test_rank_deficient_design_uses_pseudoinverse():
    result = solve([[1.,1.],[2.,2.],[3.,3.]], [2.,4.,6.])
    assert result.shape == (3,) and np.all(np.isfinite(result))
