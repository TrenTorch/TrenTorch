import numpy as np


def mse_loss(y_pred, y_true):
    """Mean squared error between predictions and targets."""
    return np.mean((y_pred - y_true) ** 2)
