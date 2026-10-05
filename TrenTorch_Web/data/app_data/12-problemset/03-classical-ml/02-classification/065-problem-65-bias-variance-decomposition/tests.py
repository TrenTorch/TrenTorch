"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    np.testing.assert_allclose(solve([[2,4],[4,6]], [3,5]), (0,1))

def test_02_case():
    np.testing.assert_allclose(solve([[1,3],[3,5]], [2,4]), (0,1))

def test_03_case():
    np.testing.assert_allclose(solve([[2,2],[2,2]], [2,2]), (0,0))

def test_04_case():
    np.testing.assert_allclose(solve([[1,2],[1,2]], [0,0]), (2.5,0))

def test_05_case():
    np.testing.assert_allclose(solve([[0,0],[2,2]], [1,1]), (0,1))

def test_06_case():
    np.testing.assert_allclose(solve([[1],[3],[5]], [3]), (0, 8/3))

def test_07_case():
    bias,var=solve([[1,2],[3,4]], [2,3])
    assert isinstance(bias,float) and isinstance(var,float)

def test_08_case():
    np.testing.assert_allclose(solve([[0,10],[2,14]], [1,12]), (0,2.5))

def test_09_case():
    np.testing.assert_allclose(solve([[1,1,1],[3,3,3]], [2,2,2]), (0,1))

def test_10_case():
    np.testing.assert_allclose(solve([[1,3],[3,5]], [2,4])[0], 0)

def test_11_case():
    np.testing.assert_allclose(solve([[2,4],[2,4],[2,4]], [2,4]), (0,0))

def test_12_case():
    np.testing.assert_allclose(solve([[-1,1],[1,3]], [0,2]), (0,1))

def test_13_case():
    np.testing.assert_allclose(solve([[0,0],[4,8]], [2,4]), (0,10))

