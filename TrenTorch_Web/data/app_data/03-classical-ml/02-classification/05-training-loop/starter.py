import numpy as np


def train_logistic_regression(
    input: np.ndarray,
    target: np.ndarray,
    lr: float,
    epochs: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    input:  shape (batch_size, in_features)
    target: shape (batch_size,), 0 or 1 per sample

    Returns:
        weight: shape (1, in_features)
        bias: shape (1,)
    """
    # TODO: Initialize weight to zeros (1, in_features), bias to zeros (1,).
    # Reshape target to (batch_size, 1) once, up front.
    # Repeat for `epochs` iterations:
    #   1. p = sigmoid(linear(input, weight, bias))
    #   2. Compute gradients with bce_gradient()
    #   3. Update weight, bias with gd_step()
    # Reuse those functions -- don't reimplement their logic here.
    pass
