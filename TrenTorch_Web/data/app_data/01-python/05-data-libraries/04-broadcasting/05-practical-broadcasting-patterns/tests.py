"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
normalize_rows = _module.normalize_rows
pairwise_differences = _module.pairwise_differences
scale_columns = _module.scale_columns


def test_normalize_rows_correctness():
    data = np.array([[1.0, 2.0, 3.0], [10.0, 20.0, 30.0]])
    result = normalize_rows(data)
    np.testing.assert_allclose(result.mean(axis=1), [0.0, 0.0], atol=1e-10)
    np.testing.assert_allclose(result.std(axis=1), [1.0, 1.0], atol=1e-10)


def test_normalize_rows_uses_keepdims_correctly():
    data = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    result = normalize_rows(data)
    assert result.shape == data.shape


def test_pairwise_differences_correctness_and_shape():
    a = np.array([1, 2, 3])
    b = np.array([10, 20])
    result = pairwise_differences(a, b)
    assert result.shape == (2, 3)
    np.testing.assert_array_equal(result, [[-9, -8, -7], [-19, -18, -17]])


def test_scale_columns_correctness():
    matrix = np.ones((4, 3))
    scale = np.array([1, 10, 100])
    result = scale_columns(matrix, scale)
    np.testing.assert_array_equal(result, np.tile(scale, (4, 1)))


def test_single_row_and_single_column_edge_cases():
    single_row = np.array([[1.0, 2.0, 3.0]])
    result = normalize_rows(single_row)
    assert result.shape == (1, 3)

    single_col_matrix = np.ones((4, 1))
    scale = np.array([5])
    result2 = scale_columns(single_col_matrix, scale)
    np.testing.assert_array_equal(result2, np.full((4, 1), 5.0))
