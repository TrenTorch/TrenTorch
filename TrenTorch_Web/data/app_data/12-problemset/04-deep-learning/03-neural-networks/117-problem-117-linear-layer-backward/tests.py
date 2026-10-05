"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    r=solve([[1,2],[3,4]],[[1],[2]],[[2],[3]])
    for a,b in zip(r, ([[2,3],[4,6]],[[7],[10]],[3])): np.testing.assert_allclose(a,b)

def test_02_case():
    r=solve([[2]],[[3]],[[4]])
    for a,b in zip(r, ([[12]],[[6]],[3])): np.testing.assert_allclose(a,b)

def test_03_case():
    r=solve([[1,0]],[[2,3]],[[1,2],[3,4]])
    for a,b in zip(r, ([[8,18]],[[2,3],[0,0]],[2,3])): np.testing.assert_allclose(a,b)

def test_04_case():
    r=solve([[1],[2],[3]],[[1],[1],[1]],[[2]])
    np.testing.assert_allclose(r[2], [3])

def test_05_case():
    r=solve([[1,2]],[[0,0]],[[2,3]])
    for a in r: np.testing.assert_array_equal(a, np.zeros_like(a))

def test_06_case():
    r=solve([[1,2],[2,3]],[[1,2],[3,4]],[[1,0],[0,1]])
    assert r[0].shape == (2,2) and r[1].shape == (2,2) and r[2].shape == (2,)

def test_07_case():
    np.testing.assert_allclose(solve([[1]],[[2]],[[3]])[1], [[2]])

def test_08_case():
    np.testing.assert_allclose(solve([[1,2],[3,4]],[[1],[1]],[[0],[2]])[1], [[4],[6]])

def test_09_case():
    np.testing.assert_allclose(solve([[1,2]],[[1,2]],[[3,4],[5,6]])[0], [[11,17]])

def test_10_case():
    np.testing.assert_allclose(solve([[0,0]],[[2]],[[1],[2]])[1], [[0],[0]])

def test_11_case():
    r=solve([[1,2]],[[3]],[[4],[5]])
    assert all(np.isfinite(v).all() for v in r)

def test_12_case():
    np.testing.assert_allclose(solve([[1],[2]],[[1],[2]],[[1]])[2], [3])

def test_13_case():
    r=solve([[1,2,3]],[[1,2]],[[1,1],[1,1],[1,1]])
    assert r[0].shape == (1,3)

