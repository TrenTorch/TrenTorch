import numpy as np


def scale_loss(loss: float, scale: float) -> float:
    return loss * scale


def unscale_gradients(gradients: list[np.ndarray], scale: float) -> list[np.ndarray]:
    return [g / scale for g in gradients]


def has_inf_or_nan(gradients: list[np.ndarray]) -> bool:
    return any(not np.all(np.isfinite(g)) for g in gradients)
