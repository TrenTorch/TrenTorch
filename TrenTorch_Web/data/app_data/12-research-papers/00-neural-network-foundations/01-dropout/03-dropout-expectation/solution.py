import numpy as np


def dropout_expectation(x, p, n_samples, rng):
    x = np.asarray(x, dtype=float)
    masks = rng.random((n_samples,) + x.shape) >= p
    return np.mean(masks * x / (1 - p), axis=0)
