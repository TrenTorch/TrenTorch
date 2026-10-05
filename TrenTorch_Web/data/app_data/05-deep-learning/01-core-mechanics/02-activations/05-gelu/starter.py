import math

import numpy as np

_erf = np.vectorize(math.erf)
_SQRT_2 = math.sqrt(2.0)
_SQRT_2PI = math.sqrt(2.0 * math.pi)


def gelu_forward(x: np.ndarray) -> np.ndarray:
    """
    Mirrors torch.nn.functional.gelu(x) (the default, exact 'none'
    approximation, not the tanh-approximate variant):

        GELU(x) = x * Phi(x)

    where Phi is the standard normal CDF, x * P(Z <= x) for Z ~ N(0, 1).
    Phi(x) is expressible via the error function:

        Phi(x) = 0.5 * (1 + erf(x / sqrt(2)))

    `_erf` (a vectorized math.erf) is already provided above.
    """
    pass


def gelu_backward(grad_output: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    Unlike relu/sigmoid/tanh/softmax, GELU's backward here takes the
    ORIGINAL INPUT x, not the saved output: GELU is not monotonic (it
    dips slightly negative for small negative x), so knowing only the
    output value cannot tell you which input produced it or what the
    local slope was there.

    d/dx GELU(x) = Phi(x) + x * phi(x)

    where phi is the standard normal PDF:

        phi(x) = exp(-x^2 / 2) / sqrt(2*pi)

    Returns grad_output * (that local derivative).
    """
    pass
