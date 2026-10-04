import numpy as np

def solve(n, k):
    """Implement k-fold indices according to the contract."""
    idx = np.arange(n)
    folds = np.array_split(idx, k)
    return [(np.concatenate([f for j, f in enumerate(folds) if j != i]), folds[i]) for i in range(k)]
