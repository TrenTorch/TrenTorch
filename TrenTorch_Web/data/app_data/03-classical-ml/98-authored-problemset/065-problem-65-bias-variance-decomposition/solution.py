import numpy as np

def solve(predictions, y):
    """Implement bias-variance decomposition according to the contract."""
    P = np.asarray(predictions, float)
    mean = P.mean(0)
    return (float(np.mean((mean - y) ** 2)), float(np.mean(np.var(P, axis=0))))
