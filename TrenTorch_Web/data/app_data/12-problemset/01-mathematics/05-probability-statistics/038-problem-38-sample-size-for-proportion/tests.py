"""Contract tests for Sample Size for Proportion."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert isinstance(solve(.10, .20), int) and solve(.10, .20) > 0
    assert solve(.50, .55) > solve(.10, .20)
def test_symmetric_inputs():
    assert solve(.2,.3) == solve(.3,.2)
def test_smaller_effect_requires_more_samples():
    assert solve(.40,.41) > solve(.40,.50)
