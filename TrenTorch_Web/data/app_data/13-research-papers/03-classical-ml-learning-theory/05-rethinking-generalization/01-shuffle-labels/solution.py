import numpy as np


def shuffle_labels(y, rng):
    return rng.permutation(np.asarray(y))
