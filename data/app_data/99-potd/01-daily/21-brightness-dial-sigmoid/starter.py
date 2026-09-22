import numpy as np


def sigmoid_forward(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Overflow-safe sigmoid, forward and backward.

    x: shape (n,), can range up to +-50.

    Return (sigma, grad):
      sigma = 1 / (1 + exp(-x))
      grad  = sigma * (1 - sigma)

    A naive 1/(1+exp(-x)) overflows for very negative x (exp(-x) blows up).
    For x < 0, use the algebraically equivalent exp(x)/(1+exp(x)) instead,
    which keeps the exponent negative.
    """
    # TODO: pick the branch by the sign of x so the exponent stays negative
    # either way.
    pass
