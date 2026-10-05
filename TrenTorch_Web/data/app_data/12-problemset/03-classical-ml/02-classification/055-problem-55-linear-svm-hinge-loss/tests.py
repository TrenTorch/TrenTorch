"""Contract tests for Linear SVM Hinge Loss."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([1,-1], [2.,-.5]) == pytest.approx(.25)
    assert solve([1,-1], [0.,0.]) == pytest.approx(1.)
def test_zero_loss_beyond_margin():
    assert solve([1,-1], [3.,-2.]) == pytest.approx(0.)
def test_misclassification_increases_loss():
    assert solve([1,-1], [-1.,1.]) == pytest.approx(2.)
