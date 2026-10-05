"""Contract tests for MAP Bernoulli Estimate."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([1, 1, 0, 1], 1., 1.) == pytest.approx(.75)
    assert solve([1, 1, 0], 2., 2.) == pytest.approx(.6)
def test_prior_symmetry():
    assert solve([0, 1], 2., 2.) == pytest.approx(.5)
def test_more_successes_raise_mode():
    assert solve([1, 1, 1], 2., 2.) > solve([0, 0, 0], 2., 2.)
