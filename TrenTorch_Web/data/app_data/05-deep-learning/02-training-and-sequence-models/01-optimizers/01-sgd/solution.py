import numpy as np


def sgd_step(params: list[np.ndarray], grads: list[np.ndarray], lr: float) -> list[np.ndarray]:
    return [param - lr * grad for param, grad in zip(params, grads)]
