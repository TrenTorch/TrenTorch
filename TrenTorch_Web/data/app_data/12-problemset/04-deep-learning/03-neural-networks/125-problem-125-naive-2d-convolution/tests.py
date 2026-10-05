"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    np.testing.assert_allclose(solve([[1,2,3],[4,5,6],[7,8,9]],[[1,0],[0,-1]]), [[-4,-4],[-4,-4]])

def test_02_case():
    np.testing.assert_allclose(solve([[1,2],[3,4]],[[1,1],[1,1]]), [[10]])

def test_03_case():
    np.testing.assert_allclose(solve([[1,2,3]],[[1,1]]), [[3,5]])

def test_04_case():
    np.testing.assert_allclose(solve([[1],[2],[3]],[[2],[1]]), [[4],[7]])

def test_05_case():
    np.testing.assert_allclose(solve([[1,2],[3,4]],[[2]]), [[2,4],[6,8]])

def test_06_case():
    np.testing.assert_array_equal(solve([[1,2,3],[4,5,6]],[[0,0],[0,0]]), np.zeros((1,2)))

def test_07_case():
    np.testing.assert_allclose(solve([[1,0],[0,1]],[[1,2],[3,4]]), [[5]])

def test_08_case():
    r=solve([[1,2,3],[4,5,6],[7,8,9]],[[1,2],[3,4]]); assert r.shape == (2,2)

def test_09_case():
    np.testing.assert_allclose(solve([[1,2,3],[4,5,6]],[[1,0,0]]), [[1],[4]])

def test_10_case():
    np.testing.assert_allclose(solve([[1,2],[3,4],[5,6]],[[1,0]]), [[1],[3],[5]])

def test_11_case():
    np.testing.assert_allclose(solve([[1,1,1],[1,1,1],[1,1,1]],[[2]]), [[2,2,2],[2,2,2],[2,2,2]])

def test_12_case():
    r=solve([[0,1,2],[3,4,5],[6,7,8]],[[1,-1],[2,0]]); assert r.shape == (2,2)

def test_13_case():
    assert np.isfinite(solve([[1,2],[3,4]],[[1,2],[3,4]])).all()

