"""Contract tests with examples and targeted valid-input cases."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

solve = load_solution('03-classical-ml/98-authored-problemset/067-problem-67-standardize-then-train').solve

def test_01_case():
    np.testing.assert_allclose(solve([[1,10],[3,14],[5,18]]), [[-np.sqrt(1.5),-np.sqrt(1.5)],[0,0],[np.sqrt(1.5),np.sqrt(1.5)]])

def test_02_case():
    np.testing.assert_allclose(solve([[2,7],[2,9]]), [[0,-1],[0,1]])

def test_03_case():
    r=solve([[4,8],[4,8]])
    np.testing.assert_array_equal(r, np.zeros((2,2)))

def test_04_case():
    r=solve([[1],[3],[5]])
    np.testing.assert_allclose(r[:,0], [-np.sqrt(1.5),0,np.sqrt(1.5)])

def test_05_case():
    r=solve([[0,2],[2,4]])
    np.testing.assert_allclose(r.mean(axis=0), [0,0], atol=1e-12)

def test_06_case():
    r=solve([[0,2],[2,4]])
    np.testing.assert_allclose(r.std(axis=0), [1,1])

def test_07_case():
    r=solve([[3,5],[3,7],[3,9]])
    np.testing.assert_array_equal(r[:,0], [0,0,0])

def test_08_case():
    r=solve([[1,2],[2,4],[3,6]])
    np.testing.assert_allclose(r[:,0], r[:,1])

def test_09_case():
    r=solve([[-1,0],[0,1],[1,2]])
    assert r.shape == (3,2)

def test_10_case():
    np.testing.assert_allclose(solve([[1,2],[1,4]])[:,0], [0,0])

def test_11_case():
    r=solve([[0,0],[1,1],[2,2]])
    np.testing.assert_allclose(r.mean(0), [0,0], atol=1e-12)

def test_12_case():
    r=solve([[2,1],[4,3]])
    np.testing.assert_allclose(r, [[-1,-1],[1,1]])

def test_13_case():
    assert np.isfinite(solve([[1,3],[5,7]])).all()

