import numpy as np


def standard_scale_no_leakage(X_train: np.ndarray, X_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X_train = np.asarray(X_train, dtype=float)
    X_test = np.asarray(X_test, dtype=float)
    mean = X_train.mean(axis=0)
    std = np.where(X_train.std(axis=0) == 0, 1.0, X_train.std(axis=0))
    return (X_train - mean) / std, (X_test - mean) / std
