import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

row_wise_attention = load_solution(
    "01-classical-ml/08-tabular-foundation-models/01-row-wise-attention"
).row_wise_attention
column_wise_attention = load_solution(
    "01-classical-ml/08-tabular-foundation-models/02-column-wise-attention"
).column_wise_attention


def two_way_attention_block(
    table: np.ndarray,
    row_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
    col_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
) -> np.ndarray:
    w_query_row, w_key_row, w_value_row = row_weights
    row_output = table + row_wise_attention(table, w_query_row, w_key_row, w_value_row)

    w_query_col, w_key_col, w_value_col = col_weights
    col_output = row_output + column_wise_attention(row_output, w_query_col, w_key_col, w_value_col)

    return col_output
