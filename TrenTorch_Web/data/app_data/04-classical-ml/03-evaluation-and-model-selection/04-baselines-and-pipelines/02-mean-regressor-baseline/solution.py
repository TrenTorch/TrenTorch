import numpy as np


def mean_regressor_baseline(y_train: np.ndarray, n_samples: int) -> np.ndarray:
    y = np.asarray(y_train, dtype=float)
    if y.size == 0:
        raise ValueError("y_train is empty, so there is no mean to predict")
    return np.full(n_samples, float(y.mean()))
