"""Contract tests for Min-Max Scaling."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/026-problem-26-min-max-scaling').solve

def test_examples():
    np.testing.assert_allclose(solve([[1.,10.],[2.,10.],[3.,10.]]), [[0.,0.],[.5,0.],[1.,0.]])
    np.testing.assert_allclose(solve([[0.,2.],[4.,6.]]), [[0.,0.],[1.,1.]])
def test_each_feature_bounds():
    result = solve([[2., 5.], [4., 9.], [6., 13.]])
    np.testing.assert_allclose(result.min(axis=0), [0.,0.])
    np.testing.assert_allclose(result.max(axis=0), [1.,1.])
def test_constant_feature():
    np.testing.assert_array_equal(solve([[7.,1.],[7.,3.]]), [[0.,0.],[0.,1.]])
