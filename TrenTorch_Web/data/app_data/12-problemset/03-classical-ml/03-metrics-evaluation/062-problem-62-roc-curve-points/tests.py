"""Contract tests for ROC Curve Points."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    result = solve([1,0,1,0], [.9,.8,.4,.1])
    np.testing.assert_allclose(result, [(0.,.5),(.5,.5),(.5,1.),(1.,1.)])
    np.testing.assert_allclose(solve([1,0,1], [.8,.8,.2]), [(1.,.5),(1.,1.)])
def test_threshold_ties_are_one_point():
    points = solve([1,0,1,0], [.7,.7,.2,.2])
    assert len(points) == 2
    np.testing.assert_allclose(points, [(.5,.5),(1.,1.)])
def test_rates_are_monotone_with_descending_thresholds():
    points = solve([1,0,1,0], [.9,.7,.3,.1])
    assert all(a[0] <= b[0] and a[1] <= b[1] for a,b in zip(points, points[1:]))
