import numpy as np

def solve(logits, labels):
    logits = np.asarray(logits, dtype=float)
    labels = np.asarray(labels, dtype=float)
    losses = np.maximum(logits, 0) - logits * labels + np.log1p(np.exp(-np.abs(logits)))
    return float(np.mean(losses))
