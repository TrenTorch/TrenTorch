"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    r=solve(2,3,7); assert r.shape == (2,3)

def test_02_case():
    np.testing.assert_array_equal(solve(1,2,0), solve(1,2,0))

def test_03_case():
    assert not np.array_equal(solve(3,3,1), solve(3,3,2))

def test_04_case():
    r=solve(4,5,9); assert r.shape == (4,5) and np.isfinite(r).all()

def test_05_case():
    r=solve(1,7,0); assert r.shape == (1,7)

def test_06_case():
    r=solve(6,1,0); assert r.shape == (6,1)

def test_07_case():
    r=solve(2,2,0); assert np.isfinite(r).all()

def test_08_case():
    r=solve(100,2,4); assert abs(r.mean()) < .3

def test_09_case():
    r=solve(5,3,42); assert r.std() > 0

def test_10_case():
    assert solve(2,3,0).dtype.kind == 'f' 

def test_11_case():
    r=solve(8,4,11); assert r.shape == (8,4)

def test_12_case():
    r=solve(1,1,5); assert np.isfinite(r[0,0])

def test_13_case():
    assert np.array_equal(solve(3,2,13), solve(3,2,13))

