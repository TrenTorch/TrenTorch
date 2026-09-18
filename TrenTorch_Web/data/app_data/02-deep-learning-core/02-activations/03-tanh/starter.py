import numpy as np


def tanh_forward(x: np.ndarray) -> np.ndarray:
    """Mirrors torch.tanh(x)."""
    pass


def tanh_backward(grad_output: np.ndarray, output: np.ndarray) -> np.ndarray:
    """
    output: the forward pass's own saved result (tanh(x)), the same
    "backward needs the output, not x" pattern 02-sigmoid uses.

    Returns:
        dL/dx = grad_output * (1 - output^2).
    """
    pass
