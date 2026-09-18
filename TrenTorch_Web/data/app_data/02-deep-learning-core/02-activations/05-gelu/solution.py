import math

import numpy as np

_erf = np.vectorize(math.erf)
_SQRT_2 = math.sqrt(2.0)
_SQRT_2PI = math.sqrt(2.0 * math.pi)


def gelu_forward(x: np.ndarray) -> np.ndarray:
    return 0.5 * x * (1.0 + _erf(x / _SQRT_2))


def gelu_backward(grad_output: np.ndarray, x: np.ndarray) -> np.ndarray:
    cdf = 0.5 * (1.0 + _erf(x / _SQRT_2))
    pdf = np.exp(-0.5 * x**2) / _SQRT_2PI
    local_grad = cdf + x * pdf
    return grad_output * local_grad
