import numpy as np


def multi_query_attention(q, k, v):
    """
    q: queries for every head, shape (H, T, d)
    k: the single shared key matrix, shape (T, d)
    v: the single shared value matrix, shape (T, d)

    Returns:
        Attention output for every head, shape (H, T, d), all heads using the same k and v.
    """
    # TODO: Score every head's queries against the shared keys, softmax, and weight the shared values (see Theory).
    pass
