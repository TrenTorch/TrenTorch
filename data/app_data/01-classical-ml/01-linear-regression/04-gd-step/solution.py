import numpy as np


def gd_step(
    weight: np.ndarray,
    bias: np.ndarray | None,
    grad_weight: np.ndarray,
    grad_bias: np.ndarray | None,
    lr: float,
) -> tuple[np.ndarray, np.ndarray | None]:
    updated_weight = weight - lr * grad_weight
    updated_bias = None if bias is None else bias - lr * grad_bias
    return updated_weight, updated_bias
