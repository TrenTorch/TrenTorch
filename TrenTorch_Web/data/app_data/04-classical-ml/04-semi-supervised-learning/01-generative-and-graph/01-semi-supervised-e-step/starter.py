import numpy as np


def responsibilities(X: np.ndarray, means: np.ndarray, covs: np.ndarray, priors: np.ndarray) -> np.ndarray:
    """
    Gaussian mixture responsibilities, shape (N, K), computed in log space.
    Raise ValueError for bad shapes, non-SPD covariances, or invalid priors.
    """
    pass


def semi_supervised_e_step(
    X: np.ndarray,
    y: np.ndarray,
    means: np.ndarray,
    covs: np.ndarray,
    priors: np.ndarray,
) -> np.ndarray:
    """
    Responsibilities with labeled rows (y >= 0) replaced by one-hot vectors.
    y uses -1 for unlabeled points.
    """
    pass
