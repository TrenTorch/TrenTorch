import numpy as np


def smote_oversample(X, n_new, k, rng):
    """
    X: minority-class samples, shape (m, d)
    n_new: number of synthetic samples to create
    k: number of nearest neighbors to choose partners from
    rng: a NumPy Generator

    Returns:
        An array of shape (n_new, d) of synthetic minority samples.
    """
    # TODO: For each new sample, pick a random minority point and one of its k neighbors, then interpolate (see Theory).
    pass
