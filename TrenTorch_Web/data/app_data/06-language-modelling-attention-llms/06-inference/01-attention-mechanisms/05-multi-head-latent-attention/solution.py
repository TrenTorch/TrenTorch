import numpy as np


def _softmax(x, axis=-1):
    x = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)


def multi_head_latent_attention(
    X: np.ndarray,
    W_Q: np.ndarray,
    W_DKV: np.ndarray,
    W_UK: np.ndarray,
    W_UV: np.ndarray,
    W_O: np.ndarray,
    n_heads: int,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    seq_len, d_model = X.shape
    d_head = d_model // n_heads

    c = X @ W_DKV
    K_full = c @ W_UK
    V_full = c @ W_UV

    Q = (X @ W_Q).reshape(seq_len, n_heads, d_head).transpose(1, 0, 2)
    K = K_full.reshape(seq_len, n_heads, d_head).transpose(1, 0, 2)
    V = V_full.reshape(seq_len, n_heads, d_head).transpose(1, 0, 2)

    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(d_head)
    if mask is not None:
        scores = np.where(np.array(mask) == 0, -np.inf, scores)
    weights = _softmax(scores, axis=-1)
    heads = weights @ V

    concat = heads.transpose(1, 0, 2).reshape(seq_len, d_model)
    output = concat @ W_O
    return output, c
