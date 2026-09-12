import numpy as np


def hinge_loss(scores: np.ndarray, target: np.ndarray, reduction: str = "mean") -> float | np.ndarray:
    elementwise = np.maximum(0.0, 1.0 - target * scores)
    if reduction == "mean":
        return float(np.mean(elementwise))
    elif reduction == "sum":
        return float(np.sum(elementwise))
    elif reduction == "none":
        return elementwise
    else:
        raise ValueError(f"Invalid reduction: {reduction!r}")
