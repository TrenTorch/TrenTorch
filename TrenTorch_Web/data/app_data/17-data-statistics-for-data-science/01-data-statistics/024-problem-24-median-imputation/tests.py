"""Contract tests for Median Imputation."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/024-problem-24-median-imputation').solve

def test_examples():
    np.testing.assert_allclose(solve([1., np.nan, 3., 4.]), [1., 3., 3., 4.])
    np.testing.assert_allclose(solve([1., np.nan, 100.]), [1., 50.5, 100.])
def test_robust_to_extreme_observation():
    np.testing.assert_allclose(solve([1., 2., np.nan, 3., 100.]), [1., 2., 2.5, 3., 100.])
def test_no_missing_values():
    np.testing.assert_array_equal(solve([3., 1., 2.]), [3., 1., 2.])
