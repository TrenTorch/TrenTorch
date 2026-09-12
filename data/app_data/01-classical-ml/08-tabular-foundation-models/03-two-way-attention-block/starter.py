import numpy as np


def two_way_attention_block(
    table: np.ndarray,
    row_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
    col_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
) -> np.ndarray:
    """
    table: shape (n_rows, n_cols, d_model).
    row_weights, col_weights: each a (w_query, w_key, w_value) tuple of
    (d_model, d_model) matrices.

    Runs row-wise attention (01), THEN column-wise attention (02) on
    its output, each with a residual connection (add the block's input
    back to its output, a real Transformer-block detail, not an
    add-on): a block with all-zero weights must leave `table` unchanged.

    Returns:
        shape (n_rows, n_cols, d_model).
    """
    # TODO: row_output = table + row_wise_attention(table, *row_weights)
    # col_output = row_output + column_wise_attention(row_output, *col_weights)
    # return col_output
    pass
