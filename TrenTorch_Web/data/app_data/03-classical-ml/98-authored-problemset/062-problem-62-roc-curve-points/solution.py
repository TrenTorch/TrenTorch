import numpy as np

def solve(y, scores):
    """Implement roc curve points according to the contract."""
    y, s = (np.asarray(y), np.asarray(scores))
    order = np.argsort(-s)
    y = y[order]
    s = s[order]
    P = np.sum(y == 1)
    N = np.sum(y == 0)
    tp = fp = 0
    out = []
    for v in s:
        m = s == v
        tp += np.sum(y[m] == 1)
        fp += np.sum(y[m] == 0)
        out.append((fp / N if N else 0, tp / P if P else 0))
    return out
