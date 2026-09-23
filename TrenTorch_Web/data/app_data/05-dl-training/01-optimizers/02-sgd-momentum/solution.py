import numpy as np


def sgd_momentum_step(
    params: list[np.ndarray],
    grads: list[np.ndarray],
    velocities: list[np.ndarray],
    lr: float,
    momentum: float = 0.9,
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    new_velocities = [momentum * v + g for v, g in zip(velocities, grads)]
    new_params = [p - lr * v for p, v in zip(params, new_velocities)]
    return new_params, new_velocities
