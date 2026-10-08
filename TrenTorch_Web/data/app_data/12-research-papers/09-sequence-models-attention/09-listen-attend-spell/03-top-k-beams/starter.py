import numpy as np


def top_k_beams(scores, k):
    """
    scores: log-probability score of each candidate hypothesis, shape (n,)
    k: beam width

    Returns:
        The indices of the k best hypotheses, best first, as Python ints.
    """
    # TODO: Sort the candidates by score descending and keep the first k indices (see Theory).
    pass
