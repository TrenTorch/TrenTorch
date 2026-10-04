"""Contract tests for Directional Derivative."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/015-problem-15-directional-derivative').solve

def test_examples():
    assert solve([2., 3.], [1., -1.]) == pytest.approx(-1/np.sqrt(2))
    assert solve([2., 3.], [1., 0.]) == pytest.approx(2.)
def test_direction_scaling():
    assert solve([2., 3.], [2., -2.]) == pytest.approx(-1/np.sqrt(2))
def test_axis_directions():
    assert solve([4., -3.], [0., 5.]) == pytest.approx(-3.)
