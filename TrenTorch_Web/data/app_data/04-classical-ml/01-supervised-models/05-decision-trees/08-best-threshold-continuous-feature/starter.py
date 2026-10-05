import numpy as np


def best_threshold(x: np.ndarray, y: np.ndarray) -> tuple:
    """
    x: 1-D float array, one continuous feature value per sample.
    y: 1-D integer array of class labels, same length as x.

    Returns:
        (threshold, gain): the midpoint threshold with the highest
        base-2 information gain, and that gain. (None, 0.0) if x has
        fewer than two distinct values.
    """
    # TODO: Score the midpoint of every consecutive pair of distinct values.
    pass
