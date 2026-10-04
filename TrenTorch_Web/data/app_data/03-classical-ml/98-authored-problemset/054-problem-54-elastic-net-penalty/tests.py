"""Contract tests for Elastic-Net Penalty."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/054-problem-54-elastic-net-penalty').solve

def test_examples():
    assert solve([1.,-2.], .5, .2) == pytest.approx(2.)
    assert solve([0.,0.], 1., 1.) == pytest.approx(0.)
def test_l1_and_l2_components():
    assert solve([2.], 1., 0.) == pytest.approx(2.)
    assert solve([2.], 0., 1.) == pytest.approx(2.)
def test_sign_invariance():
    assert solve([1.,-3.], .2, .5) == pytest.approx(solve([-1.,3.], .2, .5))
