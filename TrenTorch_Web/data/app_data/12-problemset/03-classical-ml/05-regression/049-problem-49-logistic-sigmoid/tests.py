"""Contract tests for Logistic Sigmoid."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([0.]), [.5])
    np.testing.assert_allclose(solve([2.,-2.]), [1/(1+np.exp(-2)), 1/(1+np.exp(2))])
def test_symmetry_and_monotonicity():
    result = solve([-3.,-1.,0.,1.,3.])
    assert np.all(np.diff(result) > 0)
    np.testing.assert_allclose(result[0], 1-result[-1])
def test_extreme_logits_remain_finite():
    result = solve([-1000.,1000.])
    assert np.all(np.isfinite(result))
    np.testing.assert_allclose(result, [0.,1.], atol=1e-12)
