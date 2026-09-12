import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax along the given axis."""
    # TODO: subtract the max along `axis` before exponentiating (the
    # same log-sum-exp-style stability trick used in
    # 04-gaussian-mixture's E-step), then normalize to sum to 1 along
    # that axis.
    pass


def scaled_dot_product_attention(
    query: np.ndarray, key: np.ndarray, value: np.ndarray
) -> np.ndarray:
    """
    query: shape (..., n_q, d_k)
    key:   shape (..., n_k, d_k)
    value: shape (..., n_k, d_v)

    Returns:
        shape (..., n_q, d_v): for each query position, a weighted
        average of value rows, weighted by how well that query matches
        each key.
    """
    # TODO: scores = query @ key^T / sqrt(d_k) (transpose only the last
    # two axes, np.swapaxes(key, -1, -2), so this works whether there's
    # a leading batch dimension or not). softmax the scores over the
    # last axis (over keys). Return weights @ value.
    pass


def row_wise_attention(
    table: np.ndarray, w_query: np.ndarray, w_key: np.ndarray, w_value: np.ndarray
) -> np.ndarray:
    """
    table: shape (n_rows, n_cols, d_model), one embedding vector per
    table cell.
    w_query, w_key, w_value: shape (d_model, d_model).

    Runs self-attention ACROSS the cells WITHIN each row, independently
    per row (a row's n_cols cells are the "sequence" attention runs
    over; different rows never interact here).

    Returns:
        shape (n_rows, n_cols, d_model).
    """
    # TODO: project table with each weight matrix (table @ w_query,
    # etc. -- this broadcasts correctly over the leading n_rows
    # dimension), then scaled_dot_product_attention on the projections.
    pass
