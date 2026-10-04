"""Contract tests for Robust Scaling."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/028-problem-28-robust-scaling').solve

def test_examples():
    np.testing.assert_allclose(solve([[1.],[2.],[3.],[4.]]), [[-1.],[-1/3],[1/3],[1.]])
    np.testing.assert_allclose(solve([[2.,7.],[4.,7.],[6.,7.]]), [[-1.,0.],[0.,0.],[1.,0.]])
def test_median_centering():
    result = solve([[0.],[2.],[10.]])
    assert np.median(result) == pytest.approx(0.)
def test_constant_feature():
    np.testing.assert_array_equal(solve([[5.],[5.],[5.]]), [[0.],[0.],[0.]])
