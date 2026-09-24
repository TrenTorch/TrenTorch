"""
pytest data/app_data/01-numpy/04-shape-manipulation/03-transpose/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/04-shape-manipulation/{Path(__file__).resolve().parent.name}")
transpose_2d = _module.transpose_2d
transpose_axes = _module.transpose_axes
transpose_shares_memory = _module.transpose_shares_memory


def test_transpose_2d_correctness():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    result = transpose_2d(arr)
    assert result.shape == (3, 2)
    np.testing.assert_array_equal(result, [[1, 4], [2, 5], [3, 6]])


def test_transpose_axes_correctness_for_3d_array():
    arr = np.arange(24).reshape(2, 3, 4)
    result = transpose_axes(arr, (1, 0, 2))
    assert result.shape == (3, 2, 4)
    np.testing.assert_array_equal(result, arr.transpose(1, 0, 2))


def test_transpose_shares_memory_always_reports_true():
    assert transpose_shares_memory(np.array([[1, 2], [3, 4]])) is True
    assert transpose_shares_memory(np.arange(5)) is True


def test_mutation_through_transposed_view_propagates_correctly():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    t = transpose_2d(arr)
    t[0, 1] = 99
    assert arr[1, 0] == 99
