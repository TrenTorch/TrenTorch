"""Contract tests with examples and targeted valid-input cases."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

solve = load_solution('04-deep-learning-core/98-authored-problemset/120-problem-120-xavier-initialization').solve

def test_01_case():
    r=solve(2,3,7); assert r.shape == (2,3)

def test_02_case():
    r=solve(1,1,0); b=np.sqrt(3); assert np.all(np.abs(r) <= b)

def test_03_case():
    np.testing.assert_array_equal(solve(3,2,12), solve(3,2,12))

def test_04_case():
    assert not np.array_equal(solve(3,3,1), solve(3,3,2))

def test_05_case():
    r=solve(4,5,9); bound=np.sqrt(6/9); assert np.all(r >= -bound) and np.all(r <= bound)

def test_06_case():
    r=solve(1,7,0); assert r.shape == (1,7)

def test_07_case():
    r=solve(6,1,0); assert r.shape == (6,1)

def test_08_case():
    r=solve(2,2,0); assert np.isfinite(r).all()

def test_09_case():
    r=solve(10,10,4); assert abs(r.mean()) < .5

def test_10_case():
    r=solve(2,3,42); assert np.all(np.abs(r) <= np.sqrt(6/5))

def test_11_case():
    assert solve(2,3,0).dtype.kind == 'f' 

def test_12_case():
    r=solve(3,4,5); assert r.min() >= -np.sqrt(6/7) and r.max() <= np.sqrt(6/7)

def test_13_case():
    assert solve(2,3,8).shape == (2,3)

