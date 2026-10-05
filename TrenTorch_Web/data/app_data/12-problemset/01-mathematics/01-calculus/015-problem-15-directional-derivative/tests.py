"""Contract tests for Directional Derivative."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([2., 3.], [1., -1.]) == pytest.approx(-1/np.sqrt(2))
    assert solve([2., 3.], [1., 0.]) == pytest.approx(2.)
def test_direction_scaling():
    assert solve([2., 3.], [2., -2.]) == pytest.approx(-1/np.sqrt(2))
def test_axis_directions():
    assert solve([4., -3.], [0., 5.]) == pytest.approx(-3.)
