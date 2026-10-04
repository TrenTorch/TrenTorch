"""Contract tests for Confidence Interval for Mean."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/035-problem-35-confidence-interval-for-mean').solve

def test_examples():
    lo, hi = solve([1.,2.,3.])
    assert (lo, hi) == pytest.approx((2.-1.96/np.sqrt(3), 2.+1.96/np.sqrt(3)))
    assert solve([5.,5.,5.], critical=2.) == pytest.approx((5.,5.))
def test_interval_is_centered_on_mean():
    values = [2.,4.,8.,10.]
    lo, hi = solve(values, critical=1.5)
    assert (lo + hi) / 2 == pytest.approx(np.mean(values))
def test_wider_critical_value_widens_interval():
    narrow = solve([1.,2.,5.,8.], critical=1.)
    wide = solve([1.,2.,5.,8.], critical=2.)
    assert wide[1]-wide[0] == pytest.approx(2*(narrow[1]-narrow[0]))
