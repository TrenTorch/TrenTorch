import numpy as np


def sequence_nll(probs, targets):
    """
    probs: per-step distributions over the vocabulary, shape (T, V); each row sums to 1
    targets: the correct token index at each step, shape (T,)

    Returns:
        The total negative log-likelihood of the target sequence, a float.
    """
    # TODO: Sum -log of the probability assigned to each correct token (see Theory).
    pass
