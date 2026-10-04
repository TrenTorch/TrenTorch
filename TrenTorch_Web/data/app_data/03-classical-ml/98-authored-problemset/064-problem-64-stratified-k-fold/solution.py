import numpy as np

def solve(y, k):
    """Implement stratified k-fold according to the contract."""
    y = np.asarray(y)
    fold_parts = [[] for _ in range(k)]
    for cls in np.unique(y):
        idx = np.where(y == cls)[0]
        for j, part in enumerate(np.array_split(idx, k)):
            fold_parts[j].extend(part.tolist())
    folds = [np.array(sorted(x), dtype=int) for x in fold_parts]
    return [(np.concatenate([f for j, f in enumerate(folds) if j != i]), folds[i]) for i in range(k)]
