import numpy as np

def best_binary_split(x, y):
    x, y = (np.asarray(x), np.asarray(y))
    best = None
    for t in np.unique(x)[:-1]:
        L, R = (y[x <= t], y[x > t])
        if len(L) == 0 or len(R) == 0:
            continue

        def g(z):
            _, c = np.unique(z, return_counts=True)
            p = c / len(z)
            return 1 - np.sum(p * p)
        score = len(L) / len(y) * g(L) + len(R) / len(y) * g(R)
        if best is None or score < best[0]:
            best = (score, t)
    if best is None:
        raise ValueError('split requires at least two feature values')
    return best

def solve(x, y):
    """Implement decision stump according to the contract."""
    score, t = best_binary_split(x, y)
    left, right = (np.asarray(y)[np.asarray(x) <= t], np.asarray(y)[np.asarray(x) > t])

    def mode(z):
        u, c = np.unique(z, return_counts=True)
        return u[np.argmax(c)]
    return (t, mode(left), mode(right))
