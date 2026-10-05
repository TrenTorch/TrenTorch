"""Contract tests for Ridge Objective."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([[1.],[2.]], [2.,4.], [1.], 1., .5) == pytest.approx(1.)
    assert solve([[1.],[2.]], [2.,4.], [1.], 1., 0.) == pytest.approx(.5)
def test_penalty_changes_with_weight_not_bias():
    base = solve([[0.],[0.]], [0.,0.], [0.], 2., .5)
    with_weight = solve([[0.],[0.]], [0.,0.], [2.], 2., .5)
    assert base == pytest.approx(4.)
    assert with_weight == pytest.approx(6.)
def test_zero_residual_zero_penalty():
    assert solve([[1.],[2.]], [2.,4.], [2.], 0., 0.) == pytest.approx(0.)
