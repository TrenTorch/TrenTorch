import numpy as np

def solve(y, k):
    y = np.asarray(y)
    folds = [[] for _ in range(k)]
    for label in np.unique(y):
        class_indices = np.flatnonzero(y == label)
        for position, index in enumerate(class_indices):
            folds[position % k].append(index)
    indices = np.arange(len(y))
    folds = [np.asarray(sorted(fold), dtype=int) for fold in folds]
    return [
        (
            indices[~np.isin(indices, validation)],
            validation,
        )
        for i, validation in enumerate(folds)
    ]
