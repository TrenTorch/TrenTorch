"""Contract tests for Binary Cross-Entropy."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/050-problem-50-binary-cross-entropy').solve

def test_examples():
    assert solve([0.,0.], [0,1]) == pytest.approx(np.log(2.))
    assert solve([2.,-2.], [1,0]) == pytest.approx(np.log1p(np.exp(-2.)))
def test_confident_correct_predictions_have_low_loss():
    assert solve([10.,-10.], [1,0]) < .001
    assert solve([10.,-10.], [0,1]) > 9.
def test_loss_is_mean_of_examples():
    assert solve([0.,0.], [1,1]) == pytest.approx(np.log(2.))
