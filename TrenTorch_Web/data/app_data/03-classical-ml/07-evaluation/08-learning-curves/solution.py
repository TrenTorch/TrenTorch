from typing import Callable

import numpy as np


def learning_curve(
    fit_and_evaluate_fn: Callable[[int], tuple[float, float]], train_sizes: list[int]
) -> tuple[np.ndarray, np.ndarray]:
    train_errors = []
    val_errors = []
    for n_samples in train_sizes:
        train_error, val_error = fit_and_evaluate_fn(n_samples)
        train_errors.append(train_error)
        val_errors.append(val_error)
    return np.array(train_errors), np.array(val_errors)
