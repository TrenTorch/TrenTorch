"""Contract tests for Entropy of a Distribution."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([.25, .75]) == pytest.approx(-.25*np.log2(.25)-.75*np.log2(.75))
    assert solve([1., 0.]) == pytest.approx(0.)
def test_uniform_binary_entropy():
    assert solve([.5, .5]) == pytest.approx(1.)
def test_uniform_four_way_entropy():
    assert solve([.25, .25, .25, .25]) == pytest.approx(2.)
