"""Contract tests for Rolling Mean."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/043-problem-43-rolling-mean').solve

def test_examples():
    np.testing.assert_allclose(solve([1.,2.,3.,4.], 2), [np.nan,1.5,2.5,3.5], equal_nan=True)
    np.testing.assert_allclose(solve([2.,4.,6.], 3), [np.nan,np.nan,4.], equal_nan=True)
def test_window_one():
    np.testing.assert_allclose(solve([3.,-1.,8.], 1), [3.,-1.,8.])
def test_trailing_means_use_only_current_window():
    np.testing.assert_allclose(solve([1.,3.,5.,7.,9.], 3), [np.nan,np.nan,3.,5.,7.], equal_nan=True)
