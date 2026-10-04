import numpy as np

def solve(X, labels, q, k):
    """Implement knn classification according to the contract."""
    X = np.asarray(X, float)
    labels = np.asarray(labels)
    q = np.asarray(q, float)
    d = np.sum((X - q) ** 2, axis=1)
    idx = np.argsort(d)[:k]
    vals = labels[idx]
    u, c = np.unique(vals, return_counts=True)
    return u[np.argmax(c)]
