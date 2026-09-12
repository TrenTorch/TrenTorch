import numpy as np


def grouped_query_attention(
    X: np.ndarray,
    W_Q: np.ndarray,
    W_K: np.ndarray,
    W_V: np.ndarray,
    W_O: np.ndarray,
    n_heads: int,
    n_kv_heads: int,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    """
    X: shape (seq_len, d_model)
    W_Q: shape (d_model, d_model); W_K, W_V: shape (d_model, n_kv_heads * d_head)
    n_heads divisible by n_kv_heads

    Returns output of shape (seq_len, d_model).
    """
    # TODO: Split Q into n_heads heads and K/V into n_kv_heads groups.
    # Repeat each KV group group_size = n_heads // n_kv_heads times so
    # query head h attends to KV group h // group_size. See Theory hint.
    pass
