import numpy as np


def relu_forward(x: np.ndarray) -> np.ndarray:
    """Mirrors torch.relu(x) / F.relu(x): max(0, x), elementwise."""
    pass


def relu_backward(grad_output: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    grad_output: the gradient flowing back from whatever came after this
    ReLU (dL/d(relu_output)), same shape as x.
    x: the ORIGINAL input this ReLU was applied to during the forward pass.

    Returns:
        dL/dx = grad_output * 1 where x > 0, grad_output * 0 where x <= 0
        (PyTorch's convention: the gradient at exactly x == 0 is 0).
    """
    pass
