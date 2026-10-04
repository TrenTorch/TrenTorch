"""Contract tests for Jacobian by Finite Differences."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/013-problem-13-jacobian-by-finite-differences').solve

def test_examples():
    np.testing.assert_allclose(solve(lambda z: np.array([z[0]**2, z[0]*z[1]]), [2., 3.]), [[4., 0.], [3., 2.]], atol=1e-6)
    np.testing.assert_allclose(solve(lambda z: np.array([z[0]+z[1], z[0]-z[1]]), [1., 2.]), [[1., 1.], [1., -1.]], atol=1e-6)
def test_vector_output_shape():
    result = solve(lambda z: np.array([z.sum(), z[0]*z[1], z[1]**2]), [2., 3.])
    assert result.shape == (3, 2)
    np.testing.assert_allclose(result, [[1., 1.], [3., 2.], [0., 6.]], atol=1e-6)
def test_step_size_argument():
    assert solve(lambda z: np.array([z[0]**3]), [2.], 1e-4)[0, 0] == pytest.approx(12., rel=1e-7)
