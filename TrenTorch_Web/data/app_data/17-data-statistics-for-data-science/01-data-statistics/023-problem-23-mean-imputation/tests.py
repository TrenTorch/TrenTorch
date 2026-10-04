"""Contract tests for Mean Imputation."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/023-problem-23-mean-imputation').solve

def test_examples():
    np.testing.assert_allclose(solve([1., np.nan, 3., 4.]), [1., 8/3, 3., 4.])
    np.testing.assert_allclose(solve([2., np.nan, 6.]), [2., 4., 6.])
def test_multiple_missing_entries():
    np.testing.assert_allclose(solve([np.nan, 2., np.nan, 4.]), [3., 2., 3., 4.])
def test_no_missing_values():
    np.testing.assert_array_equal(solve([1., 2., 3.]), [1., 2., 3.])
