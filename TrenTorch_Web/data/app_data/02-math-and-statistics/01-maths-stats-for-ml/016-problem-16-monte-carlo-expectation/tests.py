"""Contract tests for Monte Carlo Expectation."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/016-problem-16-monte-carlo-expectation').solve

def test_examples():
    assert solve(lambda x: x**2, [1., 2., 3.]) == pytest.approx(14/3)
    assert solve(lambda x: x, [2., 4., 6.]) == pytest.approx(4.)
def test_constant_function():
    assert solve(lambda x: np.full_like(x, 7.), [1., 2., 3.]) == pytest.approx(7.)
def test_shifted_samples():
    assert solve(lambda x: x + 1., [0., 1., 2.]) == pytest.approx(2.)
