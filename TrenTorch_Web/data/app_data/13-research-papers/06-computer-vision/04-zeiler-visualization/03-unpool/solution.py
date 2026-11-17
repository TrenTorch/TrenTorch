import numpy as np


def unpool_with_switches(pooled, switches, size):
    pooled = np.asarray(pooled, dtype=float)
    switches = np.asarray(switches, dtype=int)
    out = np.zeros(len(pooled) * size)
    out[np.arange(len(pooled)) * size + switches] = pooled
    return out
