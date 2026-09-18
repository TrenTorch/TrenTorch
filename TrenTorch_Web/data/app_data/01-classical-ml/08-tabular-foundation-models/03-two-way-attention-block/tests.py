"""
pytest data/app_data/01-classical-ml/08-tabular-foundation-models/03-two-way-attention-block/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

two_way_attention_block = load_solution(
    f"01-classical-ml/08-tabular-foundation-models/{Path(__file__).resolve().parent.name}"
).two_way_attention_block
row_wise_attention = load_solution(
    "01-classical-ml/08-tabular-foundation-models/01-row-wise-attention"
).row_wise_attention
column_wise_attention = load_solution(
    "01-classical-ml/08-tabular-foundation-models/02-column-wise-attention"
).column_wise_attention


def test_zero_weights_leave_the_table_unchanged():
    rng = np.random.default_rng(0)
    table = rng.normal(size=(3, 4, 5))
    zero_weights = tuple(np.zeros((5, 5)) for _ in range(3))
    output = two_way_attention_block(table, zero_weights, zero_weights)
    assert np.allclose(output, table)


def test_output_shape_matches_input():
    rng = np.random.default_rng(1)
    table = rng.normal(size=(3, 4, 6))
    row_weights = tuple(rng.normal(size=(6, 6)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(6, 6)) for _ in range(3))
    output = two_way_attention_block(table, row_weights, col_weights)
    assert output.shape == (3, 4, 6)


def test_nonzero_weights_actually_change_the_table():
    rng = np.random.default_rng(2)
    table = rng.normal(size=(3, 4, 5))
    row_weights = tuple(rng.normal(size=(5, 5)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(5, 5)) for _ in range(3))
    output = two_way_attention_block(table, row_weights, col_weights)
    assert not np.allclose(output, table)


def test_matches_manual_step_by_step_computation():
    rng = np.random.default_rng(3)
    table = rng.normal(size=(4, 3, 5))
    row_weights = tuple(rng.normal(size=(5, 5)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(5, 5)) for _ in range(3))

    manual_row_output = table + row_wise_attention(table, *row_weights)
    manual_col_output = manual_row_output + column_wise_attention(manual_row_output, *col_weights)

    output = two_way_attention_block(table, row_weights, col_weights)
    assert np.allclose(output, manual_col_output)


def test_column_wise_step_operates_on_the_row_wise_output_not_the_original_table():
    # Directly targets a mutant that runs column_wise_attention on the
    # ORIGINAL table instead of the row-wise step's output: with
    # nonzero row weights, these two give numerically different results,
    # so the block's actual behavior distinguishes the correct wiring.
    rng = np.random.default_rng(4)
    table = rng.normal(size=(4, 3, 5))
    row_weights = tuple(rng.normal(size=(5, 5)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(5, 5)) for _ in range(3))

    correct_row_output = table + row_wise_attention(table, *row_weights)
    wrong_col_output = table + column_wise_attention(table, *col_weights)  # bug: uses `table`

    output = two_way_attention_block(table, row_weights, col_weights)
    assert not np.allclose(output, wrong_col_output)
    assert np.allclose(
        output, correct_row_output + column_wise_attention(correct_row_output, *col_weights)
    )
