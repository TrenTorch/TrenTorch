"""Contract tests for Bayes Posterior."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/019-problem-19-bayes-posterior').solve

def test_examples():
    assert solve(.2, .8, .1) == pytest.approx(2/3)
    assert solve(.5, .2, .2) == pytest.approx(.5)
def test_strong_evidence_for_h1():
    assert solve(.1, .9, .1) == pytest.approx(.5)
def test_zero_prior():
    assert solve(0., .8, .1) == pytest.approx(0.)
