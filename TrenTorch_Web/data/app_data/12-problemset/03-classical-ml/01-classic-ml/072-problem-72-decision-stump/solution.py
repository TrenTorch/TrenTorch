import numpy as np

def solve(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)
    best = None
    for t in np.unique(x)[:-1]:
        left = y[x <= t]
        right = y[x > t]
        if len(left) == 0 or len(right) == 0:
            continue

        def gini(z):
            _, counts = np.unique(z, return_counts=True)
            p = counts / len(z)
            return 1 - np.sum(p * p)

        score = len(left) / len(y) * gini(left) + len(right) / len(y) * gini(right)
        if best is None or score < best[0]:
            best = (score, t)
    if best is None:
        raise ValueError("no valid split: x has fewer than two distinct values")
    threshold = best[1]

    def mode(z):
        values, counts = np.unique(z, return_counts=True)
        return values[np.argmax(counts)]

    left = y[x <= threshold]
    right = y[x > threshold]
    return threshold, mode(left), mode(right)
