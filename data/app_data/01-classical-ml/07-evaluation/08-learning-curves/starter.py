from typing import Callable

import numpy as np


def learning_curve(
    fit_and_evaluate_fn: Callable[[int], tuple[float, float]], train_sizes: list[int]
) -> tuple[np.ndarray, np.ndarray]:
    """
    fit_and_evaluate_fn(n_samples) -> (train_error, val_error): trains a
    model on the FIRST n_samples training points and returns both its
    training error and its (fixed, held-out) validation error.

    Returns:
        (train_errors, val_errors), each shape (len(train_sizes),),
        one entry per size in train_sizes, in order.
    """
    # TODO: Call fit_and_evaluate_fn once per size in train_sizes,
    # collecting the two error sequences.
    pass
