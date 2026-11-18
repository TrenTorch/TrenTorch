import numpy as np


def causal_conv1d(x, w):
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    out = np.zeros(len(x))
    for t in range(len(x)):
        for j in range(len(w)):
            if t - j >= 0:
                out[t] += w[j] * x[t - j]
    return out
