"""Contract tests for Two-Sample Difference in Means."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/033-problem-33-two-sample-difference-in-means').solve

def test_examples():
    assert solve([2.,4.,6.], [1.,2.,3.]) == pytest.approx(2.)
    assert solve([1.,1.], [3.,5.]) == pytest.approx(-3.)
def test_equal_means():
    assert solve([0.,2.,4.], [1.,2.,3.]) == pytest.approx(0.)
def test_difference_direction():
    assert solve([10.,12.], [2.,4.]) == pytest.approx(8.)
