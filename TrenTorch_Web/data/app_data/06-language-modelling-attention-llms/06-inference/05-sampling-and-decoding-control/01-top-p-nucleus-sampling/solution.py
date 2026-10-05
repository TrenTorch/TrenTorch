import numpy as np


def top_p_filter(probs, p):
    probs = np.asarray(probs, dtype=float)
    order = np.argsort(-probs, kind="stable")
    cum = np.cumsum(probs[order])
    cutoff = int(np.searchsorted(cum, p - 1e-12)) + 1
    keep = order[:cutoff]
    out = np.zeros_like(probs)
    out[keep] = probs[keep]
    return out / out.sum()
