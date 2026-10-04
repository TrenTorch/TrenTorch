"""Contract tests for Bootstrap Mean."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/032-problem-32-bootstrap-mean').solve

def test_examples():
    assert solve([2.,2.,2.], B=100, seed=4) == pytest.approx((2.,2.))
    assert solve([0.,0.,0.], B=100, seed=4) == pytest.approx((0.,0.))
def test_reproducible_interval():
    one = solve([1.,2.,3.,4.], B=200, alpha=.1, seed=7)
    two = solve([1.,2.,3.,4.], B=200, alpha=.1, seed=7)
    assert one == pytest.approx(two)
    assert one[0] <= one[1]
def test_interval_tracks_data_scale():
    low, high = solve([5.,5.,5.], B=50, seed=0)
    assert low == pytest.approx(5.) and high == pytest.approx(5.)
