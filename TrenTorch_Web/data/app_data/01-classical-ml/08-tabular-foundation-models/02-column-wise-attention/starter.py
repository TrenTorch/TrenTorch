import numpy as np


def column_wise_attention(
    table: np.ndarray, w_query: np.ndarray, w_key: np.ndarray, w_value: np.ndarray
) -> np.ndarray:
    """
    Same mechanism as 01-row-wise-attention's row_wise_attention, along
    the OTHER axis: runs attention ACROSS the rows WITHIN each column,
    independently per column. A cell can be influenced by other rows'
    values in the SAME column, but never by a different column.

    Returns:
        shape (n_rows, n_cols, d_model), same shape as table.
    """
    # TODO: Transpose the first two axes of table (np.swapaxes(table,
    # 0, 1)) so columns become the leading "batch" dimension and rows
    # become the sequence attention runs over. Project and run
    # scaled_dot_product_attention (reuse 01-row-wise-attention's),
    # then transpose back to the original (n_rows, n_cols, d_model)
    # layout before returning.
    pass
