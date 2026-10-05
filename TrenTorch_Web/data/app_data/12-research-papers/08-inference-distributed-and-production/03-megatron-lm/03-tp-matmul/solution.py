import numpy as np


def tensor_parallel_matmul(x, shards):
    return np.concatenate([np.asarray(x, dtype=float) @ np.asarray(s, dtype=float) for s in shards], axis=1)
