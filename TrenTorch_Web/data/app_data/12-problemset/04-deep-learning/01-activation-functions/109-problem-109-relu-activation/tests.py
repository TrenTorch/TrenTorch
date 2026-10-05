"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    np.testing.assert_array_equal(solve([-2,0,3]), [0,0,3])

def test_02_case():
    np.testing.assert_array_equal(solve([-1.5,2]), [0,2])

def test_03_case():
    np.testing.assert_array_equal(solve([0]), [0])

def test_04_case():
    np.testing.assert_array_equal(solve([-5,-1]), [0,0])

def test_05_case():
    np.testing.assert_array_equal(solve([1,4]), [1,4])

def test_06_case():
    r=solve([[-1,2],[3,-4]])
    np.testing.assert_array_equal(r, [[0,2],[3,0]])

def test_07_case():
    assert solve([-2,0,3]).shape == (3,)

def test_08_case():
    np.testing.assert_array_equal(solve([-1e20,1e20]), [0,1e20])

def test_09_case():
    np.testing.assert_allclose(solve([-.1,.1]), [0,.1])

def test_10_case():
    np.testing.assert_array_equal(solve([2]), [2])

def test_11_case():
    r=solve(np.arange(-5,6))
    assert np.all(r >= 0)

def test_12_case():
    np.testing.assert_array_equal(solve([0,-0.0]), [0,0])

def test_13_case():
    assert np.issubdtype(solve([-1,2]).dtype, np.integer)

