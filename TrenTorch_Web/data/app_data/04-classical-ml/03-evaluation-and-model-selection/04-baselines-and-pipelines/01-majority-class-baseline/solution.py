import numpy as np


def majority_class_baseline(y_train: np.ndarray, n_samples: int) -> np.ndarray:
    y_train = np.asarray(y_train)
    if y_train.size == 0:
        raise ValueError("y_train is empty, so there is no majority class")
    labels, counts = np.unique(y_train, return_counts=True)
    majority = labels[np.argmax(counts)]
    return np.full(n_samples, majority, dtype=y_train.dtype)
