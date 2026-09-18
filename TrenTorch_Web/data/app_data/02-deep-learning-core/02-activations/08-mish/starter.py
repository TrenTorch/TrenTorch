import numpy as np


def _softplus(x: np.ndarray) -> np.ndarray:
    return np.logaddexp(0.0, x)


def _sigmoid(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-clipped))


def mish_forward(x: np.ndarray) -> np.ndarray:
    """
    Mirrors torch.nn.functional.mish(x):

        Mish(x) = x * tanh(softplus(x))

    where softplus(x) = ln(1 + exp(x)) (a smooth approximation of ReLU).
    `_softplus` is already provided above, using the numerically stable
    np.logaddexp(0, x) rather than a literal log(1+exp(x)) (which
    overflows for large x the same way an unshifted softmax would).
    """
    pass


def mish_backward(grad_output: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    Like GELU and Swish, Mish is not monotonic, so backward needs the
    original input x, not the saved output.

    Let sp = softplus(x) and t = tanh(sp). Using the product and chain
    rules on Mish(x) = x * tanh(softplus(x)), and the facts that
    d/dx softplus(x) = sigmoid(x) and d/dt tanh(t) = 1 - tanh(t)^2
    (03-tanh's own backward formula):

        d/dx Mish(x) = t + x * (1 - t^2) * sigmoid(x)

    Returns grad_output * (that local derivative).
    """
    pass
