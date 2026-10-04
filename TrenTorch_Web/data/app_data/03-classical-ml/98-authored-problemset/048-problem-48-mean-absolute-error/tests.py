"""Contract tests for Mean Absolute Error."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/048-problem-48-mean-absolute-error').solve

def test_examples():
    assert solve([1.,2.,3.], [1.,4.,2.]) == pytest.approx(1.)
    assert solve([2.,2.], [2.,2.]) == pytest.approx(0.)
def test_sign_of_residual_does_not_matter():
    assert solve([0.,0.], [-2.,2.]) == pytest.approx(2.)
def test_translation_invariance():
    assert solve([1.,3.,5.], [0.,4.,7.]) == pytest.approx(solve([11.,13.,15.], [10.,14.,17.]))
