"""Contract tests for Low-Rank Reconstruction."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/010-problem-10-low-rank-reconstruction').solve

def test_examples():
    np.testing.assert_allclose(solve([[3., 0.], [0., 1.]], 1), [[3., 0.], [0., 0.]])
    np.testing.assert_allclose(solve([[1., 2.], [3., 4.]], 2), [[1., 2.], [3., 4.]], atol=1e-10)
def test_rank_one_reconstruction():
    result = solve([[1., 2.], [2., 4.]], 1)
    np.testing.assert_allclose(result, [[1., 2.], [2., 4.]], atol=1e-10)
def test_output_shape():
    assert solve([[1., 2., 3.], [4., 5., 6.]], 1).shape == (2, 3)
