from typing import Callable

import numpy as np


def validation_curve(
    fit_and_evaluate_fn: Callable[[object], tuple[float, float]], param_values: list
) -> tuple[np.ndarray, np.ndarray]:
    train_errors = []
    val_errors = []
    for param_value in param_values:
        train_error, val_error = fit_and_evaluate_fn(param_value)
        train_errors.append(train_error)
        val_errors.append(val_error)
    return np.array(train_errors), np.array(val_errors)
