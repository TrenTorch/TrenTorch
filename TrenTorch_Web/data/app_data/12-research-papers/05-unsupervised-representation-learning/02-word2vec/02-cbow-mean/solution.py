import numpy as np


def cbow_context_mean(context_vectors):
    return np.asarray(context_vectors, dtype=float).mean(axis=0)
