"""Contract tests for Time-Series Lag Feature."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([10.,20.,30.,40.]), [np.nan,10.,20.,30.], equal_nan=True)
    np.testing.assert_allclose(solve([3.,8.]), [np.nan,3.], equal_nan=True)
def test_lag_preserves_order():
    np.testing.assert_allclose(solve([5.,1.,9.,2.]), [np.nan,5.,1.,9.], equal_nan=True)
def test_single_observation():
    result = solve([7.])
    assert len(result) == 1 and np.isnan(result[0])
