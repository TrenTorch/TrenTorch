import numpy as np


def info_nce(q, k_pos, negatives, tau):
    q = np.asarray(q, dtype=float)
    q = q / np.linalg.norm(q)
    keys = np.vstack([np.asarray(k_pos, dtype=float)[None, :], np.asarray(negatives, dtype=float)])
    keys = keys / np.linalg.norm(keys, axis=1, keepdims=True)
    logits = (keys @ q) / tau
    return float(np.logaddexp.reduce(logits) - logits[0])
