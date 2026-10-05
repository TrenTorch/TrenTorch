"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    r=solve([0,1,1,0],[.1,.2,.8,.9],2)
    np.testing.assert_allclose(r, [(0.15,.5,2),(.85,.5,2)])

def test_02_case():
    assert solve([1],[1.0],2) == [(1.0,1.0,1)]

def test_03_case():
    assert solve([0],[0.0],2) == [(0.0,0.0,1)]

def test_04_case():
    assert solve([1,0],[.49,.51],2) == [(.49,1.0,1),(.51,0.0,1)]

def test_05_case():
    assert solve([1,0],[.5,1.0],2) == [(.75,.5,2)]

def test_06_case():
    assert solve([],[],3) == []

def test_07_case():
    r=solve([1,0,1],[.1,.2,.9],4)
    assert sum(row[2] for row in r) == 3

def test_08_case():
    r=solve([0,1],[.2,.8],4)
    assert len(r) == 2

def test_09_case():
    r=solve([0,1],[.25,.75],2)
    assert r[0][0] == .25 and r[1][0] == .75

def test_10_case():
    r=solve([0,1,1],[.1,.2,.3],1)
    np.testing.assert_allclose(r, [(.2,2/3,3)])

def test_11_case():
    r=solve([1,0],[.2,.3],5)
    assert r == [(.25,.5,2)]

def test_12_case():
    r=solve([0,1],[.2,.8],2)
    assert all(isinstance(row[2], int) for row in r)

def test_13_case():
    assert solve([0,1,0],[.1,.5,.9],10)[-1] == (.9,0.0,1)

