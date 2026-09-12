import numpy as np


def residual_connection(x: np.ndarray, sublayer_output: np.ndarray) -> np.ndarray:
    """
    Adds a sublayer's output back onto its own input: `x + sublayer_output`.
    """
    pass


def residual_connection_backward(grad_output: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Backward pass through a residual connection. Returns
    `(grad_x, grad_sublayer_output)`, the gradient flowing back to each
    of the addition's two inputs.
    """
    pass
