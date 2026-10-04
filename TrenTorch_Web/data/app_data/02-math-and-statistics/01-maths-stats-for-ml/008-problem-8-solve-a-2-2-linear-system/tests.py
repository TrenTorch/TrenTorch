"""Contract tests for Solve a 2×2 Linear System."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/008-problem-8-solve-a-2-2-linear-system').solve

def test_examples():
    np.testing.assert_allclose(solve([2, 1, 1, 3, 5, 7]), [1.6, 1.8])
    np.testing.assert_allclose(solve([1, 0, 0, 1, -2, 4]), [-2., 4.])
def test_substitution_satisfies_equations():
    coeffs = [3., 2., 1., 4., 7., 9.]
    x, y = solve(coeffs)
    assert 3*x + 2*y == pytest.approx(7.)
    assert x + 4*y == pytest.approx(9.)
def test_singular_system_contract():
    with pytest.raises(ValueError):
        solve([1, 2, 2, 4, 3, 6])
