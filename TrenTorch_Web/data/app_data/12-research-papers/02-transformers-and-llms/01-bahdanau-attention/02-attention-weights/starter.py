import numpy as np


def attention_weights(scores):
    """
    scores: alignment scores, shape (T,)

    Returns:
        A probability vector (softmax of the scores), shape (T,), that sums to 1.
    """
    # TODO: Apply a numerically stable softmax (see Theory).
    pass
