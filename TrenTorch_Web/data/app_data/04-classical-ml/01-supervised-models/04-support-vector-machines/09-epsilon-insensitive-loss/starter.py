import numpy as np


def epsilon_insensitive_loss(
    predictions: np.ndarray, targets: np.ndarray, epsilon: float = 0.1, reduction: str = "mean"
) -> float | np.ndarray:
    """
    Per-pair loss max(0, |prediction - target| - epsilon), reduced by
    reduction: "mean" (default), "sum", or "none" (elementwise array).
    Any other reduction raises ValueError.
    """
    pass
