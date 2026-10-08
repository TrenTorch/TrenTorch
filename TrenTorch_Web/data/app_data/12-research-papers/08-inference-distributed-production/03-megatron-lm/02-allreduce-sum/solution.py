import numpy as np


def allreduce_sum(parts):
    return np.sum(np.stack([np.asarray(p, dtype=float) for p in parts]), axis=0)
