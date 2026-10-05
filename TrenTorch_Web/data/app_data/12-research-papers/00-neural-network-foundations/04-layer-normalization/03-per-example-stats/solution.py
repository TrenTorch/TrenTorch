import numpy as np


def per_example_stats(x):
    x = np.asarray(x, dtype=float)
    return x.mean(axis=-1), x.var(axis=-1)
