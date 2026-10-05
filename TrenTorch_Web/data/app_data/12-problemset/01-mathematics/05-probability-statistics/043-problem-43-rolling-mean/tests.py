"""Contract tests for Rolling Mean."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([1.,2.,3.,4.], 2), [np.nan,1.5,2.5,3.5], equal_nan=True)
    np.testing.assert_allclose(solve([2.,4.,6.], 3), [np.nan,np.nan,4.], equal_nan=True)
def test_window_one():
    np.testing.assert_allclose(solve([3.,-1.,8.], 1), [3.,-1.,8.])
def test_trailing_means_use_only_current_window():
    np.testing.assert_allclose(solve([1.,3.,5.,7.,9.], 3), [np.nan,np.nan,3.,5.,7.], equal_nan=True)
