"""
pytest data/app_data/01-numpy/04-shape-manipulation/02-flatten-vs-ravel/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/04-shape-manipulation/{Path(__file__).resolve().parent.name}")
flatten_safe = _module.flatten_safe
flatten_efficient = _module.flatten_efficient
compare_flatten_ravel = _module.compare_flatten_ravel


def test_flatten_safe_correctness_and_independence():
    arr = np.array([[1, 2], [3, 4]])
    result = flatten_safe(arr)
    np.testing.assert_array_equal(result, [1, 2, 3, 4])
    result[0] = 99
    np.testing.assert_array_equal(arr, [[1, 2], [3, 4]])


def test_flatten_efficient_correctness():
    arr = np.array([[1, 2], [3, 4]])
    np.testing.assert_array_equal(flatten_efficient(arr), flatten_safe(arr))


def test_compare_flatten_ravel_reports_flatten_shares_memory_false():
    arr = np.array([[1, 2], [3, 4]])
    result = compare_flatten_ravel(arr)
    assert result["flatten_shares_memory"] is False


def test_compare_flatten_ravel_reports_ravel_shares_memory_true_for_contiguous():
    arr = np.array([[1, 2], [3, 4]])
    result = compare_flatten_ravel(arr)
    assert result["ravel_shares_memory"] is True


def test_3d_input_handled_correctly():
    arr = np.arange(24).reshape(2, 3, 4)
    np.testing.assert_array_equal(flatten_safe(arr), np.arange(24))
    np.testing.assert_array_equal(flatten_efficient(arr), np.arange(24))
