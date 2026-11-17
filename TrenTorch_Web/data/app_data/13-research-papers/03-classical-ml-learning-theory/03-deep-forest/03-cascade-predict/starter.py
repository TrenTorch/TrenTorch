import numpy as np


def cascade_predict(forest_probas):
    """
    forest_probas: list of arrays, one per forest in the final layer, each of shape (n, c)

    Returns:
        The predicted class for each sample, shape (n,): the argmax of the averaged class vectors.
    """
    # TODO: Average the forests' class vectors and take the argmax per sample (see Theory).
    pass
