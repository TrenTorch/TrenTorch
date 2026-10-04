"""Contract tests with examples and targeted valid-input cases."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

solve = load_solution('04-deep-learning-core/98-authored-problemset/113-problem-113-softmax-vector').solve

def test_01_case():
    np.testing.assert_allclose(solve([1,2,3]), [.0900305732,.2447284711,.6652409558])

def test_02_case():
    np.testing.assert_allclose(solve([0,0]), [.5,.5])

def test_03_case():
    np.testing.assert_allclose(solve([5]), [1])

def test_04_case():
    r=solve([-1,0,1])
    np.testing.assert_allclose(r.sum(), 1)

def test_05_case():
    r=solve([1,2,3]); assert np.all(r > 0)

def test_06_case():
    np.testing.assert_allclose(solve([1000,1001]), solve([0,1]))

def test_07_case():
    np.testing.assert_allclose(solve([-1000,0]), [0,1])

def test_08_case():
    np.testing.assert_allclose(solve([3,1,2]), solve([1,2,3])[[2,0,1]])

def test_09_case():
    assert solve([1,2,3]).shape == (3,)

def test_10_case():
    assert np.isfinite(solve([-1e6,0,1e6])).all()

def test_11_case():
    np.testing.assert_allclose(solve([-2,-2,-2]), [1/3]*3)

def test_12_case():
    r=solve([0,1]); assert np.all((r >= 0) & (r <= 1))

def test_13_case():
    np.testing.assert_allclose(solve([0,0,0]).sum(), 1)

