"""Contract tests for Bernoulli Mean and Variance."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/017-problem-17-bernoulli-mean-and-variance').solve

def test_examples():
    assert solve([0, 1, 1, 0, 1]) == pytest.approx((.6, .24))
    assert solve([1, 1, 1, 1]) == pytest.approx((1., 0.))
def test_balanced_observations():
    assert solve([0, 1, 0, 1]) == pytest.approx((.5, .25))
def test_all_failures():
    assert solve([0, 0, 0]) == pytest.approx((0., 0.))
