import numpy as np


def kmeans_plus_plus_init(X: np.ndarray, k: int, seed: int = 0) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    n = len(X)
    if not 1 <= k <= n:
        raise ValueError("k must satisfy 1 <= k <= number of samples")
    rng = np.random.default_rng(seed)
    chosen = [int(rng.integers(n))]
    d2 = np.sum((X - X[chosen[0]]) ** 2, axis=1)
    while len(chosen) < k:
        total = d2.sum()
        if total > 0:
            nxt = int(rng.choice(n, p=d2 / total))
        else:
            nxt = int(rng.integers(n))
        chosen.append(nxt)
        d2 = np.minimum(d2, np.sum((X - X[nxt]) ** 2, axis=1))
    return X[chosen].copy()
