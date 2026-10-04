"""Contract tests for Frobenius Norm."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/006-problem-6-frobenius-norm').solve

def test_examples():
    assert solve([[3., 4.], [0., 12.]]) == pytest.approx(13.)
    assert solve([[1., 2.]]) == pytest.approx(np.sqrt(5.))
def test_zero_and_sign_invariance():
    assert solve([[0., 0.], [0., 0.]]) == 0.
    assert solve([[-3., 4.]]) == pytest.approx(5.)
def test_single_entry():
    assert solve([[7.]]) == pytest.approx(7.)
