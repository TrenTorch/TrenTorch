import numpy as np


def corrected_resampled_t(diffs: np.ndarray, n_train: int, n_test: int) -> float:
    d = np.asarray(diffs, dtype=float)
    if d.ndim != 1 or d.size < 2:
        raise ValueError("diffs must be 1-D with at least two repeats")
    if n_train <= 0 or n_test <= 0:
        raise ValueError("n_train and n_test must be positive")
    var = d.var(ddof=1)
    if var == 0:
        raise ValueError("differences have zero variance, so t is undefined")
    k = d.size
    correction = 1.0 / k + n_test / n_train
    return float(d.mean() / np.sqrt(correction * var))
