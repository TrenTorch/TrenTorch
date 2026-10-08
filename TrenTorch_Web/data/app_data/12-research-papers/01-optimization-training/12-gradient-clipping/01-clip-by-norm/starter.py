import numpy as np


def clip_by_norm(g, threshold):
    """
    g: gradient vector
    threshold: maximum allowed norm

    Returns:
        The gradient rescaled to norm threshold if its norm exceeds it, otherwise unchanged.
    """
    # TODO: Rescale g to the threshold norm when it is too large (see Theory).
    pass
