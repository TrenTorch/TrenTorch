import numpy as np


def cost_sensitive_error(y_true: np.ndarray, y_pred: np.ndarray, cost_matrix: np.ndarray) -> float:
    """
    y_true, y_pred: 1-D integer class arrays of equal length.
    cost_matrix: (n_classes, n_classes); cost_matrix[i][j] is the cost of
        predicting j when the truth is i.

    Returns:
        mean cost per sample, 0.0 if there are no samples.
    """
    # TODO: Look up one cost per sample and average.
    pass
