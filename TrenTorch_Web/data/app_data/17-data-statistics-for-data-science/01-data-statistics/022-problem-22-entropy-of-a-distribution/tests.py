"""Contract tests for Entropy of a Distribution."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/022-problem-22-entropy-of-a-distribution').solve

def test_examples():
    assert solve([.25, .75]) == pytest.approx(-.25*np.log2(.25)-.75*np.log2(.75))
    assert solve([1., 0.]) == pytest.approx(0.)
def test_uniform_binary_entropy():
    assert solve([.5, .5]) == pytest.approx(1.)
def test_uniform_four_way_entropy():
    assert solve([.25, .25, .25, .25]) == pytest.approx(2.)
