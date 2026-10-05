"""Contract tests for One-Hot Encode Categories."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_array_equal(solve(["a", "b", "a"], ["a", "b", "c"]), [[1,0,0],[0,1,0],[1,0,0]])
    np.testing.assert_array_equal(solve(["green", "red"], ["red", "green"]), [[0,1],[1,0]])
def test_category_order_is_respected():
    result = solve(["x", "y"], ["y", "x"])
    np.testing.assert_array_equal(result, [[0,1],[1,0]])
def test_each_row_has_one_hot_value():
    result = solve(["a", "c", "b"], ["a", "b", "c"])
    np.testing.assert_array_equal(result.sum(axis=1), [1,1,1])
