import numpy as np


def _softmax(x, axis=-1):
    x = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)


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
    seq_len, d_model = X.shape
    d_head = d_model // n_heads
    group_size = n_heads // n_kv_heads

    Q = (X @ W_Q).reshape(seq_len, n_heads, d_head).transpose(1, 0, 2)
    K = (X @ W_K).reshape(seq_len, n_kv_heads, d_head).transpose(1, 0, 2)
    V = (X @ W_V).reshape(seq_len, n_kv_heads, d_head).transpose(1, 0, 2)

    K_rep = np.repeat(K, group_size, axis=0)
    V_rep = np.repeat(V, group_size, axis=0)

    scores = Q @ K_rep.transpose(0, 2, 1) / np.sqrt(d_head)
    if mask is not None:
        scores = np.where(np.array(mask) == 0, -np.inf, scores)
    weights = _softmax(scores, axis=-1)
    heads = weights @ V_rep

    concat = heads.transpose(1, 0, 2).reshape(seq_len, d_model)
    return concat @ W_O
