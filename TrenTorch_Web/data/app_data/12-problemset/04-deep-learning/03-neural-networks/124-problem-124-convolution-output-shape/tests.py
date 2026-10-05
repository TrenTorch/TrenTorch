"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_case():
    assert solve(7,3,1,2) == 4

def test_02_case():
    assert solve(5,3,0,1) == 3

def test_03_case():
    assert solve(3,3,0,1) == 1

def test_04_case():
    assert solve(8,3,0,1) == 6

def test_05_case():
    assert solve(8,3,1,1) == 8

def test_06_case():
    assert solve(10,4,0,2) == 4

def test_07_case():
    assert solve(10,4,1,2) == 5

def test_08_case():
    assert solve(1,1,0,1) == 1

def test_09_case():
    assert solve(5,2,0,2) == 2

def test_10_case():
    assert solve(5,2,1,2) == 3

def test_11_case():
    assert solve(10,3,0,3) == 3

def test_12_case():
    assert solve(10,3,1,3) == 4

def test_13_case():
    assert isinstance(solve(7,3,1,2), int)

