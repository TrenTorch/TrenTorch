"""Contract tests for Monte Carlo Expectation."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve(lambda x: x**2, [1., 2., 3.]) == pytest.approx(14/3)
    assert solve(lambda x: x, [2., 4., 6.]) == pytest.approx(4.)
def test_constant_function():
    assert solve(lambda x: np.full_like(x, 7.), [1., 2., 3.]) == pytest.approx(7.)
def test_shifted_samples():
    assert solve(lambda x: x + 1., [0., 1., 2.]) == pytest.approx(2.)
