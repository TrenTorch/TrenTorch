import numpy as np

def solve(X, y, batch_size, seed=0):
    """Implement mini-batch iterator according to the contract."""
    X, y = (np.asarray(X), np.asarray(y))
    idx = np.arange(len(X))
    rng = np.random.default_rng(seed)
    rng.shuffle(idx)
    return [(X[j], y[j]) for j in np.array_split(idx, int(np.ceil(len(X) / batch_size)))]
