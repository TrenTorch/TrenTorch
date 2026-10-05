import numpy as np


def fbeta_score(y_true: np.ndarray, y_pred: np.ndarray, beta: float = 1.0, positive=1) -> float:
    """
    (1 + beta^2) * P * R / (beta^2 * P + R) for the positive class.
    Precision and recall default to 0.0 when undefined. Returns 0.0 when
    the denominator is zero. Raises ValueError when beta <= 0.
    """
    pass
