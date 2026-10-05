import numpy as np


def linear_backward(
    grad_output: np.ndarray, x: np.ndarray, weight: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    The backward pass of `[01-linear-forward]`'s `linear_forward`. Given
    the upstream gradient `grad_output` (shape (batch_size, out_features)),
    the original input `x` (shape (batch_size, in_features)), and `weight`
    (shape (out_features, in_features)), returns the gradient with respect
    to each of the three things `linear_forward` reads:
    (grad_x, grad_weight, grad_bias).
    """
    pass
