import numpy as np

def solve(logits, k, rng):
    """Implement top-k sampling according to the contract."""
    z = np.asarray(logits, float).copy()
    idx = np.argpartition(z, -k)[-k:]
    keep = np.full(len(z), -1000000000.0)
    keep[idx] = z[idx]
    keep -= keep.max()
    p = np.exp(keep)
    p /= p.sum()
    return rng.choice(len(z), p=p)
