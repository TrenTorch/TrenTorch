import numpy as np


def epsilon_insensitive_loss(
    predictions: np.ndarray, targets: np.ndarray, epsilon: float = 0.1, reduction: str = "mean"
) -> float | np.ndarray:
    elementwise = np.maximum(0.0, np.abs(predictions - targets) - epsilon)
    if reduction == "mean":
        return float(np.mean(elementwise))
    elif reduction == "sum":
        return float(np.sum(elementwise))
    elif reduction == "none":
        return elementwise
    else:
        raise ValueError(f"Invalid reduction: {reduction!r}")
