import numpy as np


def expand_kv(kv, n_heads):
    """
    kv: key or value tensor with one entry per key-value head, shape (n_kv, T, d)
    n_heads: number of query heads, a multiple of n_kv

    Returns:
        The tensor repeated so each query head has its own copy, shape (n_heads, T, d).
    """
    # TODO: Repeat each key-value head for the query heads in its group (see Theory).
    pass
