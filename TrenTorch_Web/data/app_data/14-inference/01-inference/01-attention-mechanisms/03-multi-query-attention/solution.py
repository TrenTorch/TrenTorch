import numpy as np


def _softmax(x, axis=-1):
    x = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)


def multi_query_attention(
    X: np.ndarray,
    W_Q: np.ndarray,
    W_K: np.ndarray,
    W_V: np.ndarray,
    W_O: np.ndarray,
    n_heads: int,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    seq_len, d_model = X.shape
    d_head = W_K.shape[1]

    Q = (X @ W_Q).reshape(seq_len, n_heads, d_head).transpose(1, 0, 2)
    K = X @ W_K
    V = X @ W_V

    scores = Q @ K.T / np.sqrt(d_head)
    if mask is not None:
        scores = np.where(np.array(mask) == 0, -np.inf, scores)
    weights = _softmax(scores, axis=-1)
    heads = weights @ V

    concat = heads.transpose(1, 0, 2).reshape(seq_len, n_heads * d_head)
    return concat @ W_O
