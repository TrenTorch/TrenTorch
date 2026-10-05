"""Contract tests for Compute a Stable L2 Norm."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([3., 4.]) == pytest.approx(5.)
    assert solve([0., 0.]) == 0.
def test_sign_and_scale_invariance():
    assert solve([-3., -4.]) == pytest.approx(5.)
    assert solve([30., 40.]) == pytest.approx(50.)
def test_small_and_large_magnitudes():
    assert solve([1e-200, 0.]) == pytest.approx(1e-200)
    assert solve([3e150, 4e150]) == pytest.approx(5e150)
