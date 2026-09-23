from typing import Callable

import numpy as np


def validation_curve(
    fit_and_evaluate_fn: Callable[[object], tuple[float, float]], param_values: list
) -> tuple[np.ndarray, np.ndarray]:
    """
    fit_and_evaluate_fn(param_value) -> (train_error, val_error): trains
    a model with this ONE hyperparameter value (same, fixed training
    set every time) and returns both errors.

    Returns:
        (train_errors, val_errors), each shape (len(param_values),).
    """
    # TODO: Same shape as 08-learning-curves's learning_curve, sweeping
    # a hyperparameter value instead of a dataset size.
    pass
