"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    y,c=solve([[1,2]],[[1,0],[0,1]],[-1,1],[[2],[3]],[0])
    np.testing.assert_allclose(y, [[9]]); np.testing.assert_allclose(c[0], [[0,3]]); np.testing.assert_allclose(c[1], [[0,3]])

def test_02_case():
    y,c=solve([[2]],[[1]],[-1],[[4]],[1])
    np.testing.assert_allclose(y, [[5]]); np.testing.assert_allclose(c, ([[1]],[[1]]))

def test_03_case():
    y,c=solve([[0]],[[1]],[0],[[2]],[0])
    np.testing.assert_array_equal(y, [[0]]); np.testing.assert_array_equal(c[1], [[0]])

def test_04_case():
    y,c=solve([[-2]],[[1]],[0],[[3]],[1])
    np.testing.assert_allclose(y, [[1]]); np.testing.assert_array_equal(c[1], [[0]])

def test_05_case():
    y,c=solve([[1,2],[3,4]],[[1],[1]],[0],[[2]],[1])
    np.testing.assert_allclose(y, [[7],[15]])

def test_06_case():
    y,c=solve([[1]],[[1,1]],[0,0],[[2],[3]],[1])
    np.testing.assert_allclose(y, [[6]])

def test_07_case():
    y,c=solve([[1,2]],[[1],[0]],[1],[[2]],[0])
    np.testing.assert_allclose(y, [[4]])

def test_08_case():
    y,c=solve([[2]],[[1]],[0],[[1]],[0])
    assert y.shape == (1,1) and len(c) == 2

def test_09_case():
    y,c=solve([[0,1]],[[1,1],[1,1]],[0,0],[[1],[1]],[0])
    np.testing.assert_allclose(c[0], [[1,1]])

def test_10_case():
    y,c=solve([[1]],[[1]],[2],[[1]],[0])
    np.testing.assert_allclose(c[0], [[3]])

def test_11_case():
    y,c=solve([[2]],[[1]],[-3],[[1]],[0])
    np.testing.assert_array_equal(c[1], [[0]])

def test_12_case():
    y,c=solve([[2]],[[1]],[-1],[[1]],[0])
    np.testing.assert_allclose(y, [[1]])

def test_13_case():
    y,c=solve([[1],[2]],[[1,2]],[0,0],[[1],[1]],[0])
    assert np.isfinite(y).all()

