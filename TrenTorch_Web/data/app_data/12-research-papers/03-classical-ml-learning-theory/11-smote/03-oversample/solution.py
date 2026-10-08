import numpy as np


def smote_oversample(X, n_new, k, rng):
    X = np.asarray(X, dtype=float)
    m = X.shape[0]
    out = []
    for _ in range(n_new):
        i = int(rng.integers(m))
        d = np.linalg.norm(X - X[i], axis=1)
        nbrs = np.argsort(d, kind="stable")[1 : k + 1]
        j = int(rng.choice(nbrs))
        u = rng.random()
        out.append(X[i] + u * (X[j] - X[i]))
    return np.array(out).reshape(n_new, X.shape[1])
