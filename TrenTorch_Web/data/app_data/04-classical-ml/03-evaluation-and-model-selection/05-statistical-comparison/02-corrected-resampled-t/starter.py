import numpy as np


def corrected_resampled_t(diffs: np.ndarray, n_train: int, n_test: int) -> float:
    """
    Nadeau-Bengio corrected t: mean(d) / sqrt((1/k + n_test/n_train) * var(d)),
    with var using k - 1. Raise ValueError for k < 2, nonpositive sizes, or zero variance.
    """
    pass
