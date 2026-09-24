"""
pytest data/app_data/01-numpy/04-shape-manipulation/04-newaxis-expand-dims/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/04-shape-manipulation/{Path(__file__).resolve().parent.name}")
to_column_vector = _module.to_column_vector
to_row_vector = _module.to_row_vector
add_dimension_at = _module.add_dimension_at


def test_to_column_vector_correct_shape_and_values():
    arr = np.array([1, 2, 3])
    result = to_column_vector(arr)
    assert result.shape == (3, 1)
    np.testing.assert_array_equal(result.flatten(), [1, 2, 3])


def test_to_row_vector_correct_shape():
    arr = np.array([1, 2, 3])
    result = to_row_vector(arr)
    assert result.shape == (1, 3)


def test_add_dimension_at_correct_for_multiple_axis_positions():
    arr = np.zeros((3, 4))
    assert add_dimension_at(arr, 0).shape == (1, 3, 4)
    assert add_dimension_at(arr, 1).shape == (3, 1, 4)
    assert add_dimension_at(arr, 2).shape == (3, 4, 1)


def test_all_three_operations_return_views():
    arr = np.array([1, 2, 3])
    assert np.shares_memory(arr, to_column_vector(arr))
    assert np.shares_memory(arr, to_row_vector(arr))
    assert np.shares_memory(arr, add_dimension_at(arr, 0))
