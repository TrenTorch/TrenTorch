"""Contract tests for Mean Absolute Error."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([1.,2.,3.], [1.,4.,2.]) == pytest.approx(1.)
    assert solve([2.,2.], [2.,2.]) == pytest.approx(0.)
def test_sign_of_residual_does_not_matter():
    assert solve([0.,0.], [-2.,2.]) == pytest.approx(2.)
def test_translation_invariance():
    assert solve([1.,3.,5.], [0.,4.,7.]) == pytest.approx(solve([11.,13.,15.], [10.,14.,17.]))
