"""Contract tests for Linear Regression Prediction."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([[1.,2.],[3.,4.]], [1.,1.], 0.), [3.,7.])
    np.testing.assert_allclose(solve([[2.,1.]], [3.,-1.], 4.), [9.])
def test_intercept_only_effect():
    base = solve([[1.,0.],[0.,1.]], [2.,3.], 0.)
    shifted = solve([[1.,0.],[0.,1.]], [2.,3.], 5.)
    np.testing.assert_allclose(shifted-base, [5.,5.])
def test_single_feature():
    np.testing.assert_allclose(solve([[0.],[2.],[4.]], [3.], 1.), [1.,7.,13.])
