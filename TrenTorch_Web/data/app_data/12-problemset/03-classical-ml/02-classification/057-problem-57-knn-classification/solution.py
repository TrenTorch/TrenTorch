import numpy as np

def solve(X, labels, q, k):
    X = np.asarray(X, dtype=float)
    q = np.asarray(q, dtype=float)
    distances = np.sum((X - q) ** 2, axis=1)
    indices = np.argsort(distances)[:k]
    values = np.asarray(labels)[indices]
    classes, counts = np.unique(values, return_counts=True)
    return classes[np.argmax(counts)]
