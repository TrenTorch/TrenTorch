"""Contract tests for Mean Squared Error."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([1.,2.,3.], [1.,4.,2.]) == pytest.approx(5/3)
    assert solve([2.,2.], [2.,2.]) == pytest.approx(0.)
def test_squared_error_weights_large_residuals():
    assert solve([0.,0.], [1.,3.]) == pytest.approx(5.)
def test_order_does_not_change_mean():
    assert solve([1.,4.,2.], [0.,5.,2.]) == pytest.approx(2/3)
