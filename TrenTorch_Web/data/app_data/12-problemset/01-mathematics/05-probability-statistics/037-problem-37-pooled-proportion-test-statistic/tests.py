"""Contract tests for Pooled Proportion Test Statistic."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([1,0,1,1], [0,0,1,0]) == pytest.approx(np.sqrt(2.))
    assert solve([1,0,1,0], [1,0,1,0]) == pytest.approx(0.)
def test_sign_reverses_when_groups_swap():
    a, b = [1,1,1,0], [0,0,1,0]
    assert solve(a,b) == pytest.approx(-solve(b,a))
def test_identical_rate_samples():
    assert solve([1,1,0,0], [1,1,0,0]) == pytest.approx(0.)
