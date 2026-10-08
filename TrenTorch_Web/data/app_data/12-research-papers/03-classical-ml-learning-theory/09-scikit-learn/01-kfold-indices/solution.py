import numpy as np


def kfold_indices(n, k):
    folds = np.array_split(np.arange(n), k)
    out = []
    for i in range(k):
        test = folds[i]
        train = np.concatenate([folds[j] for j in range(k) if j != i])
        out.append((train, test))
    return out
