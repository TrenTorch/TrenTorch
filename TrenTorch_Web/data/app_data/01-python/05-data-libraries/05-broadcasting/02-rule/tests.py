"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
are_broadcastable = _module.are_broadcastable
broadcast_result_shape = _module.broadcast_result_shape
add_scalar = _module.add_scalar
add_row_vector = _module.add_row_vector
add_column_vector = _module.add_column_vector
outer_sum = _module.outer_sum


def test_equal_shapes_are_always_compatible():
    assert are_broadcastable((2, 3), (2, 3)) is True
    assert broadcast_result_shape((2, 3), (2, 3)) == (2, 3)


def test_size_1_dimension_stretching_in_various_positions():
    assert are_broadcastable((2, 3), (1, 3)) is True
    assert broadcast_result_shape((2, 3), (1, 3)) == (2, 3)
    assert are_broadcastable((5, 1), (5, 4)) is True
    assert broadcast_result_shape((5, 1), (5, 4)) == (5, 4)


def test_shorter_shape_correctly_padded_on_left():
    assert are_broadcastable((2, 3), (3,)) is True
    assert broadcast_result_shape((2, 3), (3,)) == (2, 3)
    assert are_broadcastable((8, 1, 6, 1), (7, 1, 5)) is True
    assert broadcast_result_shape((8, 1, 6, 1), (7, 1, 5)) == (8, 7, 6, 5)


def test_genuinely_incompatible_shapes_correctly_rejected():
    assert are_broadcastable((2, 3), (2, 4)) is False
    assert are_broadcastable((6,), (2, 3)) is False


def test_higher_dimensional_shape_compatibility():
    assert are_broadcastable((2, 1, 4, 1), (1, 3, 1, 5)) is True
    assert broadcast_result_shape((2, 1, 4, 1), (1, 3, 1, 5)) == (2, 3, 4, 5)
    assert are_broadcastable((3, 4, 5), (4, 6)) is False


def test_add_scalar_correctness():
    matrix = np.ones((2, 3))
    np.testing.assert_array_equal(add_scalar(matrix, 5), np.full((2, 3), 6.0))


def test_add_row_vector_correctness():
    matrix = np.ones((2, 3))
    row = np.array([1, 2, 3])
    np.testing.assert_array_equal(add_row_vector(matrix, row), [[2, 3, 4], [2, 3, 4]])


def test_add_column_vector_correctness():
    matrix = np.ones((3, 2))
    col = np.array([10, 20, 30])
    result = add_column_vector(matrix, col)
    np.testing.assert_array_equal(result, [[11, 11], [21, 21], [31, 31]])


def test_add_column_vector_fails_without_reshaping():
    matrix = np.ones((4, 3))
    col = np.array([10, 20, 30, 40])
    try:
        bad = matrix + col
        assert bad.shape != (4, 3) or not np.array_equal(bad, add_column_vector(matrix, col))
    except ValueError:
        pass


def test_outer_sum_correctness_and_shape():
    row_values = np.array([1, 2, 3])
    col_values = np.array([10, 20])
    result = outer_sum(row_values, col_values)
    assert result.shape == (2, 3)
    np.testing.assert_array_equal(result, [[11, 12, 13], [21, 22, 23]])
