import numpy as np


def l1_loss(input: np.ndarray, target: np.ndarray, reduction: str = "mean") -> float | np.ndarray:
    absolute_error = np.abs(input - target)
    if reduction == "mean":
        return float(np.mean(absolute_error))
    elif reduction == "sum":
        return float(np.sum(absolute_error))
    elif reduction == "none":
        return absolute_error
    else:
        raise ValueError(f"Invalid reduction: {reduction!r}")
