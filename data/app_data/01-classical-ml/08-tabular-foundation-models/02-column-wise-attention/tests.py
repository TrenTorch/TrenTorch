"""
pytest data/app_data/01-classical-ml/08-tabular-foundation-models/02-column-wise-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

column_wise_attention = load_solution(
    f"01-classical-ml/08-tabular-foundation-models/{Path(__file__).resolve().parent.name}"
).column_wise_attention
row_wise_attention = load_solution(
    "01-classical-ml/08-tabular-foundation-models/01-row-wise-attention"
).row_wise_attention
scaled_dot_product_attention = load_solution(
    "01-classical-ml/08-tabular-foundation-models/01-row-wise-attention"
).scaled_dot_product_attention


def test_output_shape_matches_input_shape():
    rng = np.random.default_rng(0)
    table = rng.normal(size=(3, 4, 6))
    w_query, w_key, w_value = (rng.normal(size=(6, 6)) for _ in range(3))
    output = column_wise_attention(table, w_query, w_key, w_value)
    assert output.shape == (3, 4, 6)


def test_columns_are_independent():
    rng = np.random.default_rng(1)
    table = rng.normal(size=(4, 3, 5))
    w_query, w_key, w_value = (rng.normal(size=(5, 5)) for _ in range(3))
    output_before = column_wise_attention(table, w_query, w_key, w_value)

    table_changed = table.copy()
    table_changed[:, 1, :] = rng.normal(size=(4, 5))
    output_after = column_wise_attention(table_changed, w_query, w_key, w_value)

    assert np.allclose(output_before[:, 0, :], output_after[:, 0, :])
    assert np.allclose(output_before[:, 2, :], output_after[:, 2, :])
    assert not np.allclose(output_before[:, 1, :], output_after[:, 1, :])


def test_matches_manual_per_column_computation():
    rng = np.random.default_rng(2)
    table = rng.normal(size=(5, 2, 4))
    w_query, w_key, w_value = (rng.normal(size=(4, 4)) for _ in range(3))
    output = column_wise_attention(table, w_query, w_key, w_value)

    for col in range(2):
        column_cells = table[:, col, :]  # shape (n_rows, d_model)
        q, k, v = column_cells @ w_query, column_cells @ w_key, column_cells @ w_value
        expected = scaled_dot_product_attention(q, k, v)
        assert np.allclose(output[:, col, :], expected)


def test_equals_row_wise_attention_on_the_transposed_table():
    # column-wise attention on a table must equal row-wise attention on
    # that table's row/column transpose, transposed back -- both share
    # the exact same underlying mechanism, just along a different axis.
    rng = np.random.default_rng(3)
    table = rng.normal(size=(4, 3, 6))
    w_query, w_key, w_value = (rng.normal(size=(6, 6)) for _ in range(3))

    column_result = column_wise_attention(table, w_query, w_key, w_value)
    transposed_table = np.swapaxes(table, 0, 1)
    row_result_on_transpose = row_wise_attention(transposed_table, w_query, w_key, w_value)

    assert np.allclose(column_result, np.swapaxes(row_result_on_transpose, 0, 1))


def test_transpose_back_is_not_dropped():
    # Directly targets a mutant that forgets to transpose the result
    # back to (n_rows, n_cols, d_model): with a non-square table
    # (different n_rows and n_cols), the shape itself would be wrong.
    rng = np.random.default_rng(4)
    table = rng.normal(size=(5, 2, 3))  # n_rows=5, n_cols=2, deliberately unequal
    w_query, w_key, w_value = (rng.normal(size=(3, 3)) for _ in range(3))
    output = column_wise_attention(table, w_query, w_key, w_value)
    assert output.shape == (5, 2, 3)
