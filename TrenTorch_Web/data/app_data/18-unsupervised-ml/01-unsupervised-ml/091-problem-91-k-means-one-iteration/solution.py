import numpy as np

def solve(X, C):
    """Implement k-means one iteration according to the contract."""
    X, C = (np.asarray(X, float), np.asarray(C, float))
    labels = np.argmin(((X[:, None, :] - C[None, :, :]) ** 2).sum(2), axis=1)
    C2 = np.array([X[labels == k].mean(0) if np.any(labels == k) else C[k] for k in range(len(C))])
    return (labels, C2)
