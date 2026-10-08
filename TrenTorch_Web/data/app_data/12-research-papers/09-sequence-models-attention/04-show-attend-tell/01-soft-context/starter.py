import numpy as np


def soft_context(alpha, feats):
    """
    alpha: attention weights over the image locations, shape (L,), summing to 1
    feats: feature vectors at each location, shape (L, D)

    Returns:
        The attention-weighted average of the features, shape (D,).
    """
    # TODO: Weight each location's features by its attention and sum them (see Theory).
    pass
