"""Contract tests for Frobenius Norm."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([[3., 4.], [0., 12.]]) == pytest.approx(13.)
    assert solve([[1., 2.]]) == pytest.approx(np.sqrt(5.))
def test_zero_and_sign_invariance():
    assert solve([[0., 0.], [0., 0.]]) == 0.
    assert solve([[-3., 4.]]) == pytest.approx(5.)
def test_single_entry():
    assert solve([[7.]]) == pytest.approx(7.)
