import numpy as np

def solve(logits, k, rng):
    z = np.asarray(logits, dtype=float).copy()
    idx = np.argpartition(z, -k)[-k:]
    keep = np.full(len(z), -1e9)
    keep[idx] = z[idx]
    keep -= keep.max()
    p = np.exp(keep)
    p /= p.sum()
    return rng.choice(len(z), p=p)
