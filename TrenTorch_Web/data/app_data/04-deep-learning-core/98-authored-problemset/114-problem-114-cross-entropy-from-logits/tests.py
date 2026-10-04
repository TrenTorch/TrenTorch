"""Contract tests with examples and targeted valid-input cases."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

solve = load_solution('04-deep-learning-core/98-authored-problemset/114-problem-114-cross-entropy-from-logits').solve

def test_01_case():
    np.testing.assert_allclose(solve([1,2,3],2), .4076059644)

def test_02_case():
    np.testing.assert_allclose(solve([0,0],0), np.log(2))

def test_03_case():
    np.testing.assert_allclose(solve([2,0],0), np.log1p(np.exp(-2)))

def test_04_case():
    np.testing.assert_allclose(solve([0,2],1), np.log1p(np.exp(-2)))

def test_05_case():
    np.testing.assert_allclose(solve([3,3,3],1), np.log(3))

def test_06_case():
    np.testing.assert_allclose(solve([1,2,3],0), np.log(np.exp(-2)+np.exp(-1)+1)+2)

def test_07_case():
    assert isinstance(solve([1,2],1), float)

def test_08_case():
    np.testing.assert_allclose(solve([-1000,1000],1), 0, atol=1e-12)

def test_09_case():
    np.testing.assert_allclose(solve([1000,0],1), 1000)

def test_10_case():
    np.testing.assert_allclose(solve([0,1000],0), 1000)

def test_11_case():
    np.testing.assert_allclose(solve([1,2,3],2), solve([11,12,13],2))

def test_12_case():
    assert solve([0,0,0,0],3) > 0

def test_13_case():
    np.testing.assert_allclose(solve([0,0,0],1), np.log(3))

