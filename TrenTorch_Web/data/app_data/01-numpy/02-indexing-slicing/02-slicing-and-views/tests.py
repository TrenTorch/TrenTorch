"""
pytest data/app_data/01-numpy/02-indexing-slicing/02-slicing-and-views/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/02-indexing-slicing/{Path(__file__).resolve().parent.name}")
slice_1d = _module.slice_1d
extract_submatrix = _module.extract_submatrix
slice_shares_memory = _module.slice_shares_memory


def test_1d_slicing_correctness_including_step():
    arr = np.arange(10)
    np.testing.assert_array_equal(slice_1d(arr, 2, 5), [2, 3, 4])
    np.testing.assert_array_equal(slice_1d(arr, 0, 10, 2), [0, 2, 4, 6, 8])
    np.testing.assert_array_equal(slice_1d(arr, 0, 10, -1), [])
    np.testing.assert_array_equal(arr[::-1], slice_1d(arr, arr.size - 1, None, -1))


def test_2d_submatrix_extraction_correctness():
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    result = extract_submatrix(arr, 0, 2, 1, 3)
    np.testing.assert_array_equal(result, [[2, 3], [5, 6]])


def test_slice_mutation_affects_original_array():
    arr = np.arange(6)
    result = slice_shares_memory(arr, 2, 5)
    assert result["original_was_affected"] is True
    assert result["original_array"][2] == -1
    assert result["slice_result"][0] == -1


def test_slice_of_a_slice_still_shares_original_buffer():
    arr = np.arange(10)
    outer = slice_1d(arr, 0, 8)
    inner = outer[2:5]
    inner[0] = -1
    assert arr[2] == -1
