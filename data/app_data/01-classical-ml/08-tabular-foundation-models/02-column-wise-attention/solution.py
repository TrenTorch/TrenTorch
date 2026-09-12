import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    "01-classical-ml/08-tabular-foundation-models/01-row-wise-attention"
).scaled_dot_product_attention


def column_wise_attention(
    table: np.ndarray, w_query: np.ndarray, w_key: np.ndarray, w_value: np.ndarray
) -> np.ndarray:
    transposed = np.swapaxes(table, 0, 1)  # (n_cols, n_rows, d_model)

    query = transposed @ w_query
    key = transposed @ w_key
    value = transposed @ w_value
    attended = scaled_dot_product_attention(query, key, value)  # (n_cols, n_rows, d_model)

    return np.swapaxes(attended, 0, 1)  # back to (n_rows, n_cols, d_model)
