"""Contract tests for A/B Conversion Rate."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([0,1,1,0], [1,1,0,1]) == pytest.approx((.5,.75,.25))
    assert solve([1,1,1], [0,1,1]) == pytest.approx((1.,2/3,-1/3))
def test_equal_rates_have_zero_lift():
    assert solve([0,1,0,1], [1,0,1,0]) == pytest.approx((.5,.5,0.))
def test_positive_and_negative_lift_signs():
    assert solve([0,0,1,0], [1,1,1,0])[2] > 0
    assert solve([1,1,1], [0,0,0])[2] < 0
