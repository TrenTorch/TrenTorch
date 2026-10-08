import numpy as np


def pointer_distribution(scores):
    """
    scores: unnormalized compatibility of the decoder state with each input position, shape (n,)

    Returns:
        A distribution over the n input positions, the softmax of the scores.
    """
    # TODO: Apply a stable softmax over the input positions (see Theory).
    pass
