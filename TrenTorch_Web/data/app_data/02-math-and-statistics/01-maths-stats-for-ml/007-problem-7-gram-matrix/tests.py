"""Contract tests for Gram Matrix."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/007-problem-7-gram-matrix').solve

def test_examples():
    np.testing.assert_allclose(solve([[1., 2.], [3., 4.]]), [[10., 14.], [14., 20.]])
    np.testing.assert_allclose(solve([[1.], [2.], [3.]]), [[14.]])
def test_symmetry_and_diagonal():
    result = solve([[1., 0.], [0., 2.], [1., 1.]])
    np.testing.assert_allclose(result, result.T)
    np.testing.assert_allclose(np.diag(result), [2., 5.])
def test_zero_matrix():
    np.testing.assert_array_equal(solve([[0., 0.], [0., 0.]]), np.zeros((2, 2)))
