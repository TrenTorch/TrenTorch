import numpy as np


def minimum_risk_class(posteriors: np.ndarray, cost_matrix: np.ndarray) -> int:
    """
    posteriors: (n_classes,) probabilities summing to 1.
    cost_matrix: (n_classes, n_classes); cost_matrix[i][j] is the cost of
        predicting class j when the true class is i.

    Returns:
        the class index with the lowest expected cost (smallest on ties).
    """
    # TODO: Compute every prediction's expected cost, return the cheapest.
    pass
