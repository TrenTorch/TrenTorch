import numpy as np

def solve(n, k):
    indices = np.arange(n)
    folds = np.array_split(indices, k)
    return [(np.concatenate([fold for j, fold in enumerate(folds) if j != i]), folds[i]) for i in range(k)]
