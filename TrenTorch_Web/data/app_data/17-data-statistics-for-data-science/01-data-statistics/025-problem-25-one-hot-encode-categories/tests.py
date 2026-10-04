"""Contract tests for One-Hot Encode Categories."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/025-problem-25-one-hot-encode-categories').solve

def test_examples():
    np.testing.assert_array_equal(solve(["a", "b", "a"], ["a", "b", "c"]), [[1,0,0],[0,1,0],[1,0,0]])
    np.testing.assert_array_equal(solve(["green", "red"], ["red", "green"]), [[0,1],[1,0]])
def test_category_order_is_respected():
    result = solve(["x", "y"], ["y", "x"])
    np.testing.assert_array_equal(result, [[0,1],[1,0]])
def test_each_row_has_one_hot_value():
    result = solve(["a", "c", "b"], ["a", "b", "c"])
    np.testing.assert_array_equal(result.sum(axis=1), [1,1,1])
