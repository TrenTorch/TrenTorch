"""Contract tests for Precision Recall."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([1,0,1,0], [1,1,0,0]) == pytest.approx((.5,.5))
    assert solve([1,1,0], [1,1,1]) == pytest.approx((2/3,1.))
def test_no_positive_predictions():
    assert solve([1,0,1], [0,0,0]) == pytest.approx((0.,0.))
def test_perfect_predictions():
    assert solve([0,1,1,0], [0,1,1,0]) == pytest.approx((1.,1.))
