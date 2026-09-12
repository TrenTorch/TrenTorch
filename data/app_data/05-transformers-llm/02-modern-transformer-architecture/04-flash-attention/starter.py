import numpy as np


def flash_attention(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    block_size: int,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    """
    Computes the exact same result as
    `[04-seq-modeling/04-attention/01-scaled-dot-product-attention]`'s
    `scaled_dot_product_attention`, WITHOUT ever materializing the full
    `(seq_len_q, seq_len_k)` attention weight matrix: processes `key`/
    `value` in chunks of `block_size` along the key axis, maintaining a
    running max, running softmax denominator, and running (unnormalized)
    output, using the "online softmax" update rule.
    """
    pass
