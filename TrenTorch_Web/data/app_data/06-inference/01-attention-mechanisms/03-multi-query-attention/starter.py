import numpy as np


def multi_query_attention(
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
    W_Q: shape (d_model, d_model); W_K, W_V: shape (d_model, d_head)
    W_O: shape (n_heads * d_head, d_model)

    Returns output of shape (seq_len, d_model).
    """
    # TODO: Split Q into n_heads heads, but compute K and V ONCE (shared
    # across every head, no reshape into a head axis). Broadcast K/V
    # against every query head in the attention matmul. See Theory.
    pass
