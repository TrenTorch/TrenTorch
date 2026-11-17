import numpy as np


def gae_advantages(deltas, gamma, lam):
    deltas = np.asarray(deltas, dtype=float)
    out = np.zeros_like(deltas)
    acc = 0.0
    for t in reversed(range(len(deltas))):
        acc = deltas[t] + gamma * lam * acc
        out[t] = acc
    return out
