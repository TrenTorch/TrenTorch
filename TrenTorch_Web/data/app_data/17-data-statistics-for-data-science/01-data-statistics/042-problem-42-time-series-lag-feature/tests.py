"""Contract tests for Time-Series Lag Feature."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/042-problem-42-time-series-lag-feature').solve

def test_examples():
    np.testing.assert_allclose(solve([10.,20.,30.,40.]), [np.nan,10.,20.,30.], equal_nan=True)
    np.testing.assert_allclose(solve([3.,8.]), [np.nan,3.], equal_nan=True)
def test_lag_preserves_order():
    np.testing.assert_allclose(solve([5.,1.,9.,2.]), [np.nan,5.,1.,9.], equal_nan=True)
def test_single_observation():
    result = solve([7.])
    assert len(result) == 1 and np.isnan(result[0])
