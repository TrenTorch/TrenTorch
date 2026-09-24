"""
pytest data/app_data/01-numpy/04-shape-manipulation/07-splitting-arrays/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/04-shape-manipulation/{Path(__file__).resolve().parent.name}")
split_into_n_parts = _module.split_into_n_parts
split_columns = _module.split_columns
split_result_shares_memory = _module.split_result_shares_memory


def test_split_into_n_parts_correctness_along_both_axes():
    arr = np.arange(12).reshape(3, 4)
    rows = split_into_n_parts(arr, 3, 0)
    assert len(rows) == 3
    assert rows[0].shape == (1, 4)
    np.testing.assert_array_equal(rows[1], [[4, 5, 6, 7]])

    cols = split_into_n_parts(arr, 2, 1)
    assert len(cols) == 2
    assert cols[0].shape == (3, 2)


def test_split_columns_correctness():
    arr = np.arange(12).reshape(3, 4)
    result = split_columns(arr, 2)
    np.testing.assert_array_equal(result[0], arr[:, :2])
    np.testing.assert_array_equal(result[1], arr[:, 2:])


def test_uneven_split_raises_error():
    arr = np.arange(10).reshape(2, 5)
    with pytest.raises(ValueError):
        split_into_n_parts(arr, 3, 1)


def test_split_result_shares_memory_reports_true():
    arr = np.arange(12).reshape(3, 4)
    assert split_result_shares_memory(arr, 3, 0) is True


def test_mutation_through_split_part_propagates_to_original():
    arr = np.arange(12).reshape(3, 4)
    parts = split_into_n_parts(arr, 3, 0)
    parts[0][0, 0] = 99
    assert arr[0, 0] == 99
