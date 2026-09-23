import numpy as np


def weighted_bce_loss(p: np.ndarray, y: np.ndarray, class_weights: dict) -> float:
    p = np.clip(p, 1e-12, 1 - 1e-12)
    weights = np.where(y == 1, class_weights[1], class_weights[0])
    losses = weights * (y * np.log(p) + (1 - y) * np.log(1 - p))
    return float(-np.mean(losses))
