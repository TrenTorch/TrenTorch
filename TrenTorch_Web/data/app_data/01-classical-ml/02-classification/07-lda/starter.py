import numpy as np


def lda_fit(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Returns (w, b) for the linear discriminant boundary, computed from
    per-class means, one shared (pooled) covariance matrix, and class priors.
    """
    # TODO: Split X by class, compute each class's mean and the pooled
    # (shared) covariance, then derive w and b from Theory's formulas.
    pass
