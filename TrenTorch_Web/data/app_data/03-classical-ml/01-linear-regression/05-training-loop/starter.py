import numpy as np


def train_linear_regression(
    input: np.ndarray,
    target: np.ndarray,
    lr: float,
    epochs: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    input:  shape (batch_size, in_features)
    target: shape (batch_size,), one target value per sample
    lr: learning rate
    epochs: number of full-batch gradient-descent steps

    Returns:
        weight: shape (1, in_features)
        bias: shape (1,)
    """
    # TODO: Initialize weight to zeros (1, in_features), bias to zeros (1,).
    # Reshape target to (batch_size, 1) once, up front.
    # Repeat for `epochs` iterations:
    #   1. Compute gradients with mse_gradient()
    #   2. Update weight, bias with gd_step()
    # Reuse those functions -- don't reimplement their logic here.
    pass
