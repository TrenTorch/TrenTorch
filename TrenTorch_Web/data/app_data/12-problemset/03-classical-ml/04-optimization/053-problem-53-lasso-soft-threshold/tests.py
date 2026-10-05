"""Contract tests for Lasso Soft Threshold."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve(3., 1.) == pytest.approx(2.)
    assert solve(-.5, 1.) == pytest.approx(0.)
def test_sign_is_preserved():
    assert solve(-4., 1.) == pytest.approx(-3.)
def test_threshold_and_zero():
    assert solve(1., 1.) == pytest.approx(0.)
    assert solve(0., 2.) == pytest.approx(0.)
