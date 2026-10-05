"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    np.testing.assert_allclose(solve([1,2,3],[1,4,2]), 5/3)

def test_02_case():
    np.testing.assert_allclose(solve([0,0],[1,-1]), 1)

def test_03_case():
    np.testing.assert_allclose(solve([2],[5]), 9)

def test_04_case():
    np.testing.assert_allclose(solve([1,2],[1,2]), 0)

def test_05_case():
    np.testing.assert_allclose(solve([1,1,1],[0,0,0]), 1)

def test_06_case():
    np.testing.assert_allclose(solve([-1,1],[-2,2]), 1)

def test_07_case():
    assert isinstance(solve([0,1],[1,0]), float)

def test_08_case():
    np.testing.assert_allclose(solve([[1,2],[3,4]],[[2,2],[2,5]]), .75)

def test_09_case():
    np.testing.assert_allclose(solve([0,0,0],[0,0,3]), 3)

def test_10_case():
    np.testing.assert_allclose(solve([1,2,3],[2,3,4]), 1)

def test_11_case():
    np.testing.assert_allclose(solve([1,2],[3,4]), 4)

def test_12_case():
    np.testing.assert_allclose(solve([0,0,0,0],[2,2,2,2]), 4)

def test_13_case():
    assert solve([1,2,3],[1,4,2]) >= 0

