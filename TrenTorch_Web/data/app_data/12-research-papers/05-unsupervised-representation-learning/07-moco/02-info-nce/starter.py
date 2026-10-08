import numpy as np


def info_nce(q, k_pos, negatives, tau):
    """
    q: query vector, shape (d,)
    k_pos: the positive key, shape (d,)
    negatives: negative keys from the queue, shape (K, d)
    tau: temperature

    Returns:
        The InfoNCE loss with L2-normalized vectors, as a float.
    """
    # TODO: Normalize the query and keys, form the logits, and apply the softmax loss (see Theory).
    pass
