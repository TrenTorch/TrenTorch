"""Contract tests with examples and targeted valid-input cases."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

solve = load_solution('04-deep-learning-core/98-authored-problemset/124-problem-124-convolution-output-shape').solve

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

