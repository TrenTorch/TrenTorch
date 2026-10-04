"""Contract tests for Sample Size for Proportion."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/038-problem-38-sample-size-for-proportion').solve

def test_examples():
    assert isinstance(solve(.10, .20), int) and solve(.10, .20) > 0
    assert solve(.50, .55) > solve(.10, .20)
def test_symmetric_inputs():
    assert solve(.2,.3) == solve(.3,.2)
def test_smaller_effect_requires_more_samples():
    assert solve(.40,.41) > solve(.40,.50)
