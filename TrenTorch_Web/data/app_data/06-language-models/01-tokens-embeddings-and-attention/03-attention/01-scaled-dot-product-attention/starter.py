import numpy as np


def scaled_dot_product_attention(
    query: np.ndarray, key: np.ndarray, value: np.ndarray, mask: np.ndarray | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    The core attention operation: for every position in `query`, compute
    a weighted average of `value`, where the weights come from how well
    that position's query vector matches every position's own key
    vector. `query`/`key`/`value` all share a shape ending in
    (seq_len, d_k) (with any number of leading batch/head dimensions).

    `mask`, if given, is ADDED to the raw similarity scores before the
    softmax (an additive mask of large negative numbers, like -inf, at
    positions that should never be attended to, `0` everywhere else,
    exactly `[02-causal-mask]`'s output).

    Returns (output, attention_weights): output has the same shape as
    `query`; attention_weights has shape (..., seq_len_q, seq_len_k),
    one row of weights per query position, each row summing to 1.
    """
    d_k = query.shape[-1]
    pass
