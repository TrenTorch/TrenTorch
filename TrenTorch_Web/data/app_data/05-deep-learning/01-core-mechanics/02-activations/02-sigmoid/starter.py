import numpy as np


def sigmoid_forward(x: np.ndarray) -> np.ndarray:
    """Mirrors torch.sigmoid(x): 1 / (1 + exp(-x)). Clip x before exponentiating for numerical stability."""
    pass


def sigmoid_backward(grad_output: np.ndarray, output: np.ndarray) -> np.ndarray:
    """
    grad_output: dL/d(sigmoid_output).
    output: the FORWARD PASS'S OWN OUTPUT (sigmoid(x)), not x itself.

    Returns:
        dL/dx = grad_output * output * (1 - output).

    Sigmoid's derivative, f'(x) = f(x)*(1-f(x)), is written entirely in
    terms of f(x) itself -- the forward pass's saved output is enough,
    there's no need to keep the original x around at all, or recompute
    sigmoid a second time.
    """
    pass
