"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    np.testing.assert_allclose(solve([2,3],3), [[2,4,8],[3,9,27]])

def test_02_case():
    np.testing.assert_allclose(solve([-1,0],2), [[-1,1],[0,0]])

def test_03_case():
    np.testing.assert_allclose(solve([2],1), [[2]])

def test_04_case():
    np.testing.assert_allclose(solve([1,2],1), [[1],[2]])

def test_05_case():
    np.testing.assert_allclose(solve([1,2],0), np.empty((2,0)))

def test_06_case():
    np.testing.assert_allclose(solve([0,3],3), [[0,0,0],[3,9,27]])

def test_07_case():
    np.testing.assert_allclose(solve([-2,2],4), [[-2,4,-8,16],[2,4,8,16]])

def test_08_case():
    r=solve([1.5],3)
    np.testing.assert_allclose(r, [[1.5,2.25,3.375]])

def test_09_case():
    r=solve([2,4],2)
    assert r.shape == (2,2)

def test_10_case():
    np.testing.assert_allclose(solve([-3],2), [[-3,9]])

def test_11_case():
    r=solve([1,2,3],3)
    np.testing.assert_allclose(r[:,0], [1,2,3])

def test_12_case():
    r=solve([1,2],4)
    np.testing.assert_allclose(r[:,-1], [1,16])

def test_13_case():
    np.testing.assert_allclose(solve([0],2), [[0,0]])

