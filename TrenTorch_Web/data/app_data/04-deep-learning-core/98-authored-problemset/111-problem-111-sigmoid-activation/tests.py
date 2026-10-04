"""Contract tests with examples and targeted valid-input cases."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

solve = load_solution('04-deep-learning-core/98-authored-problemset/111-problem-111-sigmoid-activation').solve

def test_01_case():
    np.testing.assert_allclose(solve([-1,0,1]), [0.2689414214,.5,.7310585786])

def test_02_case():
    np.testing.assert_allclose(solve([-1000,1000]), [0,1])

def test_03_case():
    np.testing.assert_allclose(solve([0]), [.5])

def test_04_case():
    np.testing.assert_allclose(solve([-2]), [1/(1+np.exp(2))])

def test_05_case():
    np.testing.assert_allclose(solve([2]), [1/(1+np.exp(-2))])

def test_06_case():
    r=solve([-4,0,4])
    assert np.all((r >= 0) & (r <= 1))

def test_07_case():
    r=solve([-3,3])
    np.testing.assert_allclose(r.sum(), 1, atol=.1)

def test_08_case():
    np.testing.assert_allclose(solve([-1,1]), 1-solve([1,-1]))

def test_09_case():
    assert solve([-10,10]).shape == (2,)

def test_10_case():
    np.testing.assert_allclose(solve([-50]), [0], atol=1e-20)

def test_11_case():
    np.testing.assert_allclose(solve([50]), [1])

def test_12_case():
    r=solve(np.array([-2.,0.,2.]))
    assert np.isfinite(r).all()

def test_13_case():
    np.testing.assert_allclose(solve([0,0]), [.5,.5])

