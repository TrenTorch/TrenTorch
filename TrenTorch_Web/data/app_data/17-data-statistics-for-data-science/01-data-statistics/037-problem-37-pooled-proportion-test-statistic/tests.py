"""Contract tests for Pooled Proportion Test Statistic."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/037-problem-37-pooled-proportion-test-statistic').solve

def test_examples():
    assert solve([1,0,1,1], [0,0,1,0]) == pytest.approx(np.sqrt(2.))
    assert solve([1,0,1,0], [1,0,1,0]) == pytest.approx(0.)
def test_sign_reverses_when_groups_swap():
    a, b = [1,1,1,0], [0,0,1,0]
    assert solve(a,b) == pytest.approx(-solve(b,a))
def test_identical_rate_samples():
    assert solve([1,1,0,0], [1,1,0,0]) == pytest.approx(0.)
