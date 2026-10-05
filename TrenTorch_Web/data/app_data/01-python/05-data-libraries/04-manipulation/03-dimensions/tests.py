"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
to_column_vector = _module.to_column_vector
to_row_vector = _module.to_row_vector
add_dimension_at = _module.add_dimension_at
remove_all_singleton_dims = _module.remove_all_singleton_dims
remove_singleton_at = _module.remove_singleton_at


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


def test_remove_all_singleton_dims_correctness():
    arr = np.zeros((1, 3, 1, 4))
    assert remove_all_singleton_dims(arr).shape == (3, 4)


def test_remove_singleton_at_correctness_for_specific_axis():
    arr = np.zeros((1, 3, 1, 4))
    assert remove_singleton_at(arr, 0).shape == (3, 1, 4)


def test_no_op_case():
    arr = np.zeros((3, 4))
    assert remove_all_singleton_dims(arr).shape == (3, 4)


def test_values_preserved_exactly():
    arr = np.arange(12).reshape(1, 3, 4)
    result = remove_all_singleton_dims(arr)
    np.testing.assert_array_equal(result, arr.reshape(3, 4))
