"""
pytest tests.py
"""

import numpy as np
import pytest
from _load import load_solution

_module = load_solution(__file__)
join_along_existing_axis = _module.join_along_existing_axis
stack_as_new_axis = _module.stack_as_new_axis
side_by_side = _module.side_by_side
stacked_vertically = _module.stacked_vertically
split_into_n_parts = _module.split_into_n_parts
split_columns = _module.split_columns
split_result_shares_memory = _module.split_result_shares_memory


def test_join_along_existing_axis_correctness_for_axis_0_and_1():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6]])
    result0 = join_along_existing_axis([a, b], 0)
    np.testing.assert_array_equal(result0, [[1, 2], [3, 4], [5, 6]])

    c = np.array([[1], [2]])
    result1 = join_along_existing_axis([a, c], 1)
    np.testing.assert_array_equal(result1, [[1, 2, 1], [3, 4, 2]])


def test_stack_as_new_axis_introduces_genuinely_new_dimension():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    result = stack_as_new_axis([a, b])
    assert result.shape == (2, 3)
    assert result.ndim == a.ndim + 1


def test_concatenate_vs_stack_produce_different_dimensionality_on_same_1d_inputs():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    concatenated = join_along_existing_axis([a, b], 0)
    stacked = stack_as_new_axis([a, b])
    assert concatenated.ndim == 1
    assert stacked.ndim == 2


def test_side_by_side_and_stacked_vertically_correctness():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    np.testing.assert_array_equal(side_by_side(a, b), [[1, 2, 5, 6], [3, 4, 7, 8]])
    np.testing.assert_array_equal(
        stacked_vertically(a, b), [[1, 2], [3, 4], [5, 6], [7, 8]]
    )


def test_all_four_functions_produce_independent_copies():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])

    result = side_by_side(a, b)
    result[0, 0] = -1
    np.testing.assert_array_equal(a, [[1, 2], [3, 4]])

    result = stacked_vertically(a, b)
    result[0, 0] = -1
    np.testing.assert_array_equal(a, [[1, 2], [3, 4]])

    result = stack_as_new_axis([a, b])
    result[0, 0, 0] = -1
    np.testing.assert_array_equal(a, [[1, 2], [3, 4]])


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
