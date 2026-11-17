"""Contract tests for F1 Score."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve(.5,.5) == pytest.approx(.5)
    assert solve(1.,0.) == pytest.approx(0.)
def test_perfect_precision_and_recall():
    assert solve(1.,1.) == pytest.approx(1.)
def test_harmonic_mean_is_bounded_by_inputs():
    value = solve(.4,.8)
    assert value == pytest.approx(8/15)
    assert .4 <= value <= .8
