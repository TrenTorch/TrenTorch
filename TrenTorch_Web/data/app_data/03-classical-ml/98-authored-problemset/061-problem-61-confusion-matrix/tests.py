"""Contract tests for Confusion Matrix."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/061-problem-61-confusion-matrix').solve

def test_examples():
    np.testing.assert_array_equal(solve([0,0,1,1], [0,1,0,1]), [[1,1],[1,1]])
    np.testing.assert_array_equal(solve([1,1,0], [1,0,0]), [[1,0],[1,1]])
def test_matrix_counts_every_observation():
    y, pred = [0,1,1,1,0], [0,0,1,0,1]
    result = solve(y,pred)
    assert result.sum() == len(y)
    np.testing.assert_array_equal(result, [[1,1],[2,1]])
def test_perfect_classifier():
    np.testing.assert_array_equal(solve([0,1,0,1], [0,1,0,1]), [[2,0],[0,2]])
