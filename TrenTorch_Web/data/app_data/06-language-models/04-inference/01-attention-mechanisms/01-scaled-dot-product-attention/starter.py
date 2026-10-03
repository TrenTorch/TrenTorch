import numpy as np


def scaled_dot_product_attention(
    Q: np.ndarray, K: np.ndarray, V: np.ndarray, mask: np.ndarray | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Q: shape (seq_len_q, d_k)
    K: shape (seq_len_k, d_k)
    V: shape (seq_len_k, d_v)
    mask: optional 0/1 array broadcastable to (seq_len_q, seq_len_k)

    Returns (output, weights): output has shape (seq_len_q, d_v), weights
    has shape (seq_len_q, seq_len_k) and each row sums to 1.
    """
    # TODO: Implement scaled dot-product attention from Theory.
    # Scale scores by 1/sqrt(d_k), apply the mask (as -inf) before the
    # softmax, and use a numerically stable softmax (subtract the row max).
    pass
