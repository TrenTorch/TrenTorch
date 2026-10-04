"""Contract tests for Gradient of a Quadratic."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/012-problem-12-gradient-of-a-quadratic').solve

def test_examples():
    np.testing.assert_allclose(solve([[2., 0.], [0., 4.]], [1., 2.], [1., -1.]), [3., 7.])
    np.testing.assert_allclose(solve([[0., 0.], [0., 0.]], [3., 4.], [2., -2.]), [2., -2.])
def test_symmetric_quadratic():
    np.testing.assert_allclose(solve([[1., 2.], [2., 3.]], [2., -1.], [0., 0.]), [0., 1.])
def test_uses_symmetric_part():
    np.testing.assert_allclose(solve([[1., 4.], [0., 2.]], [2., 3.], [1., 1.]), [9., 11.])
