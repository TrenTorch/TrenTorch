"""Contract tests for Matrix-Vector Product."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/004-problem-4-matrix-vector-product').solve

def test_examples():
    np.testing.assert_allclose(solve([[1., 2.], [3., 4.]], [1., 2.]), [5., 11.])
    np.testing.assert_allclose(solve([[2., -1.]], [3., 4.]), [2.])
def test_rectangular_matrix():
    np.testing.assert_allclose(solve([[1., 0., 2.], [-1., 3., 1.]], [2., 1., 4.]), [10., 5.])
def test_zero_vector():
    np.testing.assert_allclose(solve([[2., 1.], [0., -3.]], [0., 0.]), [0., 0.])
