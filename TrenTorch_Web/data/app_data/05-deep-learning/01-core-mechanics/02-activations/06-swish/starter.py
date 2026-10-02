import numpy as np


def _sigmoid(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-clipped))


def swish_forward(x: np.ndarray) -> np.ndarray:
    """
    Mirrors torch.nn.functional.silu(x) (Swish and SiLU are the same
    function, sigmoid-weighted linear unit):

        Swish(x) = x * sigmoid(x)

    `_sigmoid` is already provided above.
    """
    pass


def swish_backward(grad_output: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    Like GELU, Swish's backward needs the original input x, not the
    saved output: Swish also dips slightly negative for small negative
    x (around x=-1.28) and is not monotonic there, so the output alone
    does not pin down the local slope.

    Using the product rule on x * sigmoid(x), with s = sigmoid(x):

        d/dx Swish(x) = s + x * s * (1 - s)

    Returns grad_output * (that local derivative).
    """
    pass
