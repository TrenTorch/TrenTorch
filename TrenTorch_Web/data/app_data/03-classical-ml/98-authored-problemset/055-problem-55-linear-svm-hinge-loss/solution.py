import numpy as np

def solve(y, scores):
    """Implement linear svm hinge loss according to the contract."""
    y = np.asarray(y)
    s = np.asarray(scores)
    return float(np.mean(np.maximum(0, 1 - y * s)))
