import numpy as np


def scalar_gradient_chain(depth: int, layer_scale: float) -> float:
    return layer_scale**depth


def matrix_gradient_norms(
    depth: int, dim: int, weight_std: float, rng: np.random.RandomState
) -> list[float]:
    grad = np.ones(dim)
    norms = [float(np.linalg.norm(grad))]
    for _ in range(depth):
        weight = rng.randn(dim, dim) * weight_std
        grad = weight @ grad
        norms.append(float(np.linalg.norm(grad)))
    return norms
