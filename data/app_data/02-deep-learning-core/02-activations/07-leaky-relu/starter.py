import numpy as np


def leaky_relu_forward(x: np.ndarray, negative_slope: float = 0.01) -> np.ndarray:
    """
    Mirrors torch.nn.functional.leaky_relu(x, negative_slope=0.01):

        LeakyReLU(x) = x            if x > 0
                     = slope * x    otherwise

    Unlike plain ReLU, negative inputs are scaled by a small slope
    instead of being zeroed out entirely.
    """
    pass


def leaky_relu_backward(
    grad_output: np.ndarray, x: np.ndarray, negative_slope: float = 0.01
) -> np.ndarray:
    """
    d/dx LeakyReLU(x) = 1     if x > 0
                       = slope otherwise

    (Same convention 01-relu uses at x == 0: treat it as the x <= 0
    branch, so LeakyReLU's boundary derivative there is `slope`, not 1.)

    Returns grad_output * (that local derivative).
    """
    pass
