"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    np.testing.assert_allclose(solve([[1,3],[2,6]],[1,2],[0,1],0), [[-1,3],[-1,3]])

def test_02_case():
    np.testing.assert_allclose(solve([[2,2]],[3,4],[1,-1]), [[1,-1]])

def test_03_case():
    np.testing.assert_allclose(solve([[0,2]],[1,1],[0,0],0), [[-1,1]])

def test_04_case():
    r=solve([[1,3,5]],[1,1,1],[0,0,0],0); np.testing.assert_allclose(r, [[-np.sqrt(1.5),0,np.sqrt(1.5)]])

def test_05_case():
    r=solve([[1,2],[3,4]],[1,1],[0,0],0); assert r.shape == (2,2)

def test_06_case():
    np.testing.assert_allclose(solve([[1,2],[3,4]],[2,2],[1,-1],0), [[-1,1],[ -1,1]])

def test_07_case():
    np.testing.assert_allclose(solve([[4,4]],[2,5],[0,0],1e-5), [[0,0]])

def test_08_case():
    r=solve([[1,2],[2,4]],[1,1],[0,0]); assert np.isfinite(r).all()

def test_09_case():
    np.testing.assert_allclose(solve([[1,5]],[1,1],[0,0],0), [[-1,1]])

def test_10_case():
    r=solve([[0,1,2],[2,3,4]],[1,1,1],[0,0,0],0); np.testing.assert_allclose(r.mean(axis=1), [0,0])

def test_11_case():
    np.testing.assert_allclose(solve([[3,3]],[2,4],[1,-1]), [[1,-1]])

def test_12_case():
    r=solve([[1,2,3]],[1,1,1],[0,0,0],1e-5); assert r.shape == (1,3)

def test_13_case():
    np.testing.assert_allclose(solve([[2,6]],[3,4],[1,-1],0), [[-2,3]])

