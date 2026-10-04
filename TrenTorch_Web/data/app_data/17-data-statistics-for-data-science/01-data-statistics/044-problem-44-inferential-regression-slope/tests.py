"""Contract tests for Inferential Regression Slope."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/044-problem-44-inferential-regression-slope').solve

def test_examples():
    assert solve([1.,2.,3.], [2.,4.,5.]) == pytest.approx((1.5, 2/3))
    assert solve([0.,1.,2.], [3.,5.,7.]) == pytest.approx((2.,3.))
def test_predictions_pass_through_mean():
    x, y = np.array([1.,3.,4.,8.]), np.array([2.,5.,6.,13.])
    slope, intercept = solve(x,y)
    assert intercept + slope*x.mean() == pytest.approx(y.mean())
def test_translation_of_response_changes_intercept_only():
    slope1, intercept1 = solve([1.,2.,4.], [2.,3.,7.])
    slope2, intercept2 = solve([1.,2.,4.], [12.,13.,17.])
    assert slope2 == pytest.approx(slope1)
    assert intercept2 == pytest.approx(intercept1 + 10.)
