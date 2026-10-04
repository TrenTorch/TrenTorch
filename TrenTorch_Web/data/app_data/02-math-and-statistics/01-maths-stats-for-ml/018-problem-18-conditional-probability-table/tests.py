"""Contract tests for Conditional Probability Table."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/018-problem-18-conditional-probability-table').solve

def test_examples():
    assert solve([True, True, False, False], [True, False, True, False]) == pytest.approx(.5)
    assert solve([True, False, True], [True, True, False]) == pytest.approx(.5)
def test_all_conditioning_cases_satisfy_event():
    assert solve([True, True, False], [True, True, False]) == pytest.approx(1.)
def test_no_conditioning_observations():
    assert solve([True, False], [False, False]) == 0.
