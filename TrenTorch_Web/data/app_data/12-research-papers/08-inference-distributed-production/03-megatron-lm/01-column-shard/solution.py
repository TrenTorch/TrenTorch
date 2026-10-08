import numpy as np


def column_shard(W, world):
    return np.split(np.asarray(W, dtype=float), world, axis=1)
