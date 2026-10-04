"""Contract tests for Compute a Stable L2 Norm."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/001-problem-1-compute-a-stable-l2-norm').solve

def test_examples():
    assert solve([3., 4.]) == pytest.approx(5.)
    assert solve([0., 0.]) == 0.
def test_sign_and_scale_invariance():
    assert solve([-3., -4.]) == pytest.approx(5.)
    assert solve([30., 40.]) == pytest.approx(50.)
def test_small_and_large_magnitudes():
    assert solve([1e-200, 0.]) == pytest.approx(1e-200)
    assert solve([3e150, 4e150]) == pytest.approx(5e150)
