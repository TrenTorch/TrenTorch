import numpy as np


def expand_kv(kv, n_heads):
    n_kv = kv.shape[0]
    return np.repeat(np.asarray(kv, dtype=float), n_heads // n_kv, axis=0)
