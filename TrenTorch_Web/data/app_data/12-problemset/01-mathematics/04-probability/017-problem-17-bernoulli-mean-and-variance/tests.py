"""Contract tests for Bernoulli Mean and Variance."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([0, 1, 1, 0, 1]) == pytest.approx((.6, .24))
    assert solve([1, 1, 1, 1]) == pytest.approx((1., 0.))
def test_balanced_observations():
    assert solve([0, 1, 0, 1]) == pytest.approx((.5, .25))
def test_all_failures():
    assert solve([0, 0, 0]) == pytest.approx((0., 0.))
