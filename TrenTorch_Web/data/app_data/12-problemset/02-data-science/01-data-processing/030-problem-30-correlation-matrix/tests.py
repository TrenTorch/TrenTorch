"""Contract tests for Correlation Matrix."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([[1.,2.],[2.,4.],[3.,6.]]), [[1.,1.],[1.,1.]])
    np.testing.assert_allclose(solve([[1.,4.],[2.,2.],[3.,0.]]), [[1.,-1.],[-1.,1.]])
def test_correlation_matrix_symmetry():
    result = solve([[1.,2.,4.],[2.,1.,3.],[4.,5.,0.],[3.,7.,2.]])
    np.testing.assert_allclose(result, result.T)
    np.testing.assert_allclose(np.diag(result), [1.,1.,1.])
def test_uncorrelated_columns():
    np.testing.assert_allclose(solve([[-1.,1.],[0.,-2.],[1.,1.]]), [[1.,0.],[0.,1.]])
