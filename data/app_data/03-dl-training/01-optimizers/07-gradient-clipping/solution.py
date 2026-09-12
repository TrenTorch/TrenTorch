import numpy as np


def compute_global_norm(grads: list[np.ndarray]) -> float:
    return float(np.sqrt(sum(np.sum(g**2) for g in grads)))


def clip_grad_norm(grads: list[np.ndarray], max_norm: float) -> list[np.ndarray]:
    total_norm = compute_global_norm(grads)
    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1.0:
        return [g * clip_coef for g in grads]
    return [g.copy() for g in grads]
