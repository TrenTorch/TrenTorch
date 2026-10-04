"""Contract tests for SVM Subgradient Step."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/056-problem-56-svm-subgradient-step').solve

def test_examples():
    np.testing.assert_allclose(solve([[1.],[-1.]], [1,-1], [0.], .1, 1.), [.2])
    np.testing.assert_allclose(solve([[1.],[-1.]], [1,-1], [2.], .1, 1.), [1.8])
def test_only_violating_margins_contribute():
    result = solve([[1.],[-1.]], [1,-1], [3.], .1, 1.)
    np.testing.assert_allclose(result, [2.7])
def test_update_does_not_mutate_input_weights():
    weights = np.array([0.])
    solve([[1.]], [1], weights, .1, .5)
    np.testing.assert_array_equal(weights, [0.])
