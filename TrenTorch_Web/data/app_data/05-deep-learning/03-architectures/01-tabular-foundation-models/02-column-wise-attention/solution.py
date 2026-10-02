
import numpy as np

from _load import load_solution

scaled_dot_product_attention = load_solution("tabular-foundation-models-row-wise-attention").scaled_dot_product_attention


def column_wise_attention(
    table: np.ndarray, w_query: np.ndarray, w_key: np.ndarray, w_value: np.ndarray
) -> np.ndarray:
    transposed = np.swapaxes(table, 0, 1)  # (n_cols, n_rows, d_model)

    query = transposed @ w_query
    key = transposed @ w_key
    value = transposed @ w_value
    attended = scaled_dot_product_attention(query, key, value)  # (n_cols, n_rows, d_model)

    return np.swapaxes(attended, 0, 1)  # back to (n_rows, n_cols, d_model)
