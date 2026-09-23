import numpy as np


def multi_head_attention(
    X: np.ndarray,
    W_Q: np.ndarray,
    W_K: np.ndarray,
    W_V: np.ndarray,
    W_O: np.ndarray,
    n_heads: int,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    """
    X: shape (seq_len, d_model)
    W_Q, W_K, W_V, W_O: shape (d_model, d_model)
    n_heads: d_model must be divisible by n_heads

    Returns output of shape (seq_len, d_model).
    """
    # TODO: Split X's projections into n_heads heads, run scaled
    # dot-product attention independently per head, concatenate, then
    # apply W_O. See Theory for the reshape/transpose trick that avoids
    # a Python loop over heads.
    pass
