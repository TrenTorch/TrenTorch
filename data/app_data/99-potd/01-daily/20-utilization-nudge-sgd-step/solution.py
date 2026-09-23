import numpy as np


def sgd_step(theta: np.ndarray, grad: np.ndarray, eta: float) -> np.ndarray:
    return theta - eta * grad
