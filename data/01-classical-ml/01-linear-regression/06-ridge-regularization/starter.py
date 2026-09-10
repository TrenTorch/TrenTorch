import numpy as np


def ridge_grad(
    X: np.ndarray, y_hat: np.ndarray, y: np.ndarray, w: np.ndarray, lam: float
) -> tuple[np.ndarray, float]:
    """
    Compute the gradient of the MSE loss with L2 regularization.
    """
    # TODO: Start from mse_grad()'s result, then add the L2 penalty
    # term to dw only. Leave db unchanged -- bias is never regularized.
    pass
