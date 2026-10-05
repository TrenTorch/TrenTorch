"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    np.testing.assert_array_equal(solve([-1,0,2]), [0,0,1])

def test_02_case():
    np.testing.assert_array_equal(solve([.5,-.5]), [1,0])

def test_03_case():
    np.testing.assert_array_equal(solve([0]), [0])

def test_04_case():
    np.testing.assert_array_equal(solve([-2,-1]), [0,0])

def test_05_case():
    np.testing.assert_array_equal(solve([1,4]), [1,1])

def test_06_case():
    np.testing.assert_array_equal(solve([[-1,2],[3,-4]]), [[0,1],[1,0]])

def test_07_case():
    assert solve([-1,0,1]).shape == (3,)

def test_08_case():
    np.testing.assert_array_equal(solve([-1e10,1e10]), [0,1])

def test_09_case():
    np.testing.assert_array_equal(solve([-.1,.1]), [0,1])

def test_10_case():
    np.testing.assert_array_equal(solve([2]), [1])

def test_11_case():
    np.testing.assert_array_equal(solve(np.arange(-5,6)), [0,0,0,0,0,0,1,1,1,1,1])

def test_12_case():
    assert solve([-1,0,1]).dtype == float

def test_13_case():
    np.testing.assert_array_equal(solve([0,-0.0]), [0,0])

