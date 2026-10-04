"""Contract tests for Z-Score Scaling."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/027-problem-27-z-score-scaling').solve

def test_examples():
    np.testing.assert_allclose(solve([[1.,5.],[2.,5.],[3.,5.]]), [[-np.sqrt(1.5),0.],[0.,0.],[np.sqrt(1.5),0.]])
    np.testing.assert_allclose(solve([[2.],[4.]]), [[-1.],[1.]])
def test_column_means_and_scales():
    result = solve([[1.,2.],[3.,4.],[5.,6.]])
    np.testing.assert_allclose(result.mean(axis=0), [0.,0.], atol=1e-12)
    np.testing.assert_allclose(result.std(axis=0), [1.,1.])
def test_constant_columns_are_zero():
    np.testing.assert_array_equal(solve([[2.,3.],[2.,3.]]), [[0.,0.],[0.,0.]])
