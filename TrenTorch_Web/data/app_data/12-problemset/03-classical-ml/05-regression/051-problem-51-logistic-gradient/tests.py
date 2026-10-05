"""Contract tests for Logistic Gradient."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    dw, db = solve([[1.],[1.]], [1,0], [0.])
    np.testing.assert_allclose(dw, [0.])
    assert db == pytest.approx(0.)
    dw, db = solve([[1.],[2.]], [1,1], [0.])
    np.testing.assert_allclose(dw, [-.75])
    assert db == pytest.approx(-.5)
def test_gradient_matches_finite_difference():
    X = np.array([[1.,2.],[-1.,1.],[2.,0.]])
    y = np.array([1.,0.,1.])
    w = np.array([.2,-.3])
    dw, db = solve(X,y,w)
    def loss(weights, bias):
        z = X @ weights + bias
        return np.mean(np.logaddexp(0., z) - y*z)
    h = 1e-6
    numeric = np.array([(loss(w+np.eye(2)[j]*h,0)-loss(w-np.eye(2)[j]*h,0))/(2*h) for j in range(2)])
    np.testing.assert_allclose(dw, numeric, atol=1e-6)
    assert db == pytest.approx((loss(w,h)-loss(w,-h))/(2*h), abs=1e-6)
def test_zero_features_give_zero_weight_gradient():
    dw, db = solve([[0.,0.],[0.,0.]], [0.,1.], [3.,-2.])
    np.testing.assert_array_equal(dw, [0.,0.])
    assert db == pytest.approx(0.)
