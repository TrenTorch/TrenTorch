"""Contract tests for MLE of Gaussian Mean."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/020-problem-20-mle-of-gaussian-mean').solve

def test_examples():
    assert solve([1., 2., 3.]) == pytest.approx(2.)
    assert solve([-2., 4.]) == pytest.approx(1.)
def test_constant_samples():
    assert solve([5., 5., 5.]) == pytest.approx(5.)
def test_translation_equivariance():
    assert solve([1., 3., 5.]) + 10 == pytest.approx(solve([11., 13., 15.]))
