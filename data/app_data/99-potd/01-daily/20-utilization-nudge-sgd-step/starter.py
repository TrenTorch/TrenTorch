import numpy as np


def sgd_step(theta: np.ndarray, grad: np.ndarray, eta: float) -> np.ndarray:
    """
    One plain SGD parameter update.

    theta: current parameters, shape (d,).
    grad: gradient at theta, shape (d,).
    eta: learning rate.

    Return theta - eta * grad, elementwise, as a vectorized operation (no
    per-element Python loop, even at d = 10^4).
    """
    # TODO: one elementwise multiply, one elementwise subtract.
    pass
