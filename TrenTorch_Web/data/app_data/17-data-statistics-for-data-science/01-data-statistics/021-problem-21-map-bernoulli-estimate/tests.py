"""Contract tests for MAP Bernoulli Estimate."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/021-problem-21-map-bernoulli-estimate').solve

def test_examples():
    assert solve([1, 1, 0, 1], 1., 1.) == pytest.approx(.75)
    assert solve([1, 1, 0], 2., 2.) == pytest.approx(.6)
def test_prior_symmetry():
    assert solve([0, 1], 2., 2.) == pytest.approx(.5)
def test_more_successes_raise_mode():
    assert solve([1, 1, 1], 2., 2.) > solve([0, 0, 0], 2., 2.)
