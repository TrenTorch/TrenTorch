import numpy as np


def chi2_statistic(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x)
    y = np.asarray(y)
    if x.ndim != 1 or x.shape != y.shape or len(x) == 0:
        raise ValueError("x and y must be non-empty 1-D arrays of the same length")
    _, x_idx = np.unique(x, return_inverse=True)
    _, y_idx = np.unique(y, return_inverse=True)
    O = np.zeros((x_idx.max() + 1, y_idx.max() + 1))
    np.add.at(O, (x_idx, y_idx), 1)
    N = O.sum()
    E = np.outer(O.sum(axis=1), O.sum(axis=0)) / N
    return float(np.sum((O - E) ** 2 / E))
