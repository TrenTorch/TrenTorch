import numpy as np


def rand_index(labels_a: np.ndarray, labels_b: np.ndarray) -> float:
    a = np.asarray(labels_a)
    b = np.asarray(labels_b)
    n = a.size
    if n < 2:
        return 1.0
    same_a = a[:, None] == a[None, :]
    same_b = b[:, None] == b[None, :]
    upper = np.triu_indices(n, k=1)
    return float(np.mean(same_a[upper] == same_b[upper]))
