"""Contract tests for Power Iteration."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/009-problem-9-power-iteration').solve

def test_examples():
    np.testing.assert_allclose(solve([[2., 0.], [0., 1.]], 20), [1., 0.], atol=1e-5)
    np.testing.assert_allclose(solve([[1., 0.], [0., 3.]], 20), [0., 1.], atol=1e-5)
def test_result_is_normalized():
    result = solve([[4., 1.], [1., 2.]], 100)
    assert np.linalg.norm(result) == pytest.approx(1.)
    np.testing.assert_allclose(np.array([[4., 1.], [1., 2.]]) @ result, (3 + np.sqrt(2)) * result, atol=1e-5)
def test_zero_operator():
    np.testing.assert_array_equal(solve([[0., 0.], [0., 0.]], 3), [0., 0.])
