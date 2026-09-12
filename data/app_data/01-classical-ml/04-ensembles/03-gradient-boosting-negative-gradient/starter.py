import numpy as np


def negative_gradient(targets: np.ndarray, predictions: np.ndarray) -> np.ndarray:
    """
    Negative gradient of squared-error loss L = 0.5*(target - prediction)^2
    with respect to prediction, evaluated at the current predictions.
    For squared error this is exactly the residual: target - prediction.
    """
    # TODO: one line.
    pass


def fit_tree_to_negative_gradient(
    input: np.ndarray,
    targets: np.ndarray,
    predictions: np.ndarray,
    max_depth: int,
) -> dict:
    """
    Fits one regression tree (05-regression-trees's build_regression_tree)
    to predict the negative gradient (the residual) of the current
    predictions, rather than the original targets directly.
    """
    # TODO: Compute the residuals with negative_gradient(), then
    # build_regression_tree() on (input, residuals).
    pass
