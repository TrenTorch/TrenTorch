import numpy as np


def enqueue(queue, new_keys, K):
    return np.concatenate([np.asarray(queue, dtype=float), np.asarray(new_keys, dtype=float)])[-K:]
