"""Contract tests for Finite Difference Derivative."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve(lambda z: z*z, 3.) == pytest.approx(6., abs=1e-6)
    assert solve(np.sin, 0.) == pytest.approx(1., abs=1e-6)
def test_cubic_and_default_step():
    assert solve(lambda z: z**3, 2., 1e-4) == pytest.approx(12., rel=1e-7)
    assert solve(lambda z: z**2, -4.) == pytest.approx(-8., abs=1e-6)
def test_constant_function():
    assert solve(lambda z: 7., 2.) == pytest.approx(0.)
