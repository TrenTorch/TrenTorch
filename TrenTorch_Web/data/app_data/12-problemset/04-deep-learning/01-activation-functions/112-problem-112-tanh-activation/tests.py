"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    np.testing.assert_allclose(solve([-1,0,1]), [-.7615941559,0,.7615941559])

def test_02_case():
    np.testing.assert_allclose(solve([0]), [0])

def test_03_case():
    np.testing.assert_allclose(solve([-2]), [np.tanh(-2)])

def test_04_case():
    np.testing.assert_allclose(solve([2]), [np.tanh(2)])

def test_05_case():
    np.testing.assert_allclose(solve([-3,3]), -solve([3,-3]))

def test_06_case():
    r=solve([-5,0,5])
    assert np.all(np.abs(r) <= 1)

def test_07_case():
    np.testing.assert_allclose(solve([-100,100]), [-1,1])

def test_08_case():
    assert solve([1,2]).shape == (2,)

def test_09_case():
    np.testing.assert_allclose(solve([-.5,.5]), [-np.tanh(.5),np.tanh(.5)])

def test_10_case():
    assert np.isfinite(solve([-1000,1000])).all()

def test_11_case():
    np.testing.assert_allclose(solve([0,0]), [0,0])

def test_12_case():
    np.testing.assert_allclose(solve([1]), [np.tanh(1)])

def test_13_case():
    r=solve(np.array([-1.,1.]))
    assert r.dtype.kind == 'f' and r.shape == (2,)

