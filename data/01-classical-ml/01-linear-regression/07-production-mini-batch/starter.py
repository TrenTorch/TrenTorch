import numpy as np


def train_linear_regression_production(
    X: np.ndarray, y: np.ndarray, lr: float, epochs: int, batch_size: int
) -> tuple[np.ndarray, float]:
    """
    Mini-batch gradient descent, reusing linear_forward / mse_grad / gd_step
    per batch instead of once per epoch over the full dataset.
    """
    # TODO: Each epoch, shuffle the sample order, split into batches of
    # batch_size, and take one gradient step per batch (not per epoch).
    # The last batch may be smaller -- handle that without crashing.
    pass
