"""Contract tests for Logistic Sigmoid."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/049-problem-49-logistic-sigmoid').solve

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
