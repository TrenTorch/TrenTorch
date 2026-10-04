"""Contract tests for Lasso Soft Threshold."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/053-problem-53-lasso-soft-threshold').solve

def test_examples():
    assert solve(3., 1.) == pytest.approx(2.)
    assert solve(-.5, 1.) == pytest.approx(0.)
def test_sign_is_preserved():
    assert solve(-4., 1.) == pytest.approx(-3.)
def test_threshold_and_zero():
    assert solve(1., 1.) == pytest.approx(0.)
    assert solve(0., 2.) == pytest.approx(0.)
