import numpy as np

def solve(y, scores):
    y = np.asarray(y, dtype=float)
    scores = np.asarray(scores, dtype=float)
    return float(np.mean(np.maximum(0.0, 1.0 - y * scores)))
