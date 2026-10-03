import numpy as np


def softmax_forward(x: np.ndarray) -> np.ndarray:
    """
    Mirrors torch.softmax(x, dim=-1): softmax over the last axis, for a
    batch of rows (x can be 1D or 2D, last axis is the "classes" axis).

    Subtract the row max before exponentiating (the standard
    numerical-stability trick, exp of a large positive number overflows,
    but shifting by the max never changes the result since it cancels
    in the numerator/denominator ratio).
    """
    pass


def softmax_backward(grad_output: np.ndarray, output: np.ndarray) -> np.ndarray:
    """
    output: the forward pass's own saved softmax result.

    Unlike relu/sigmoid/tanh, softmax's Jacobian is NOT diagonal, every
    output element depends on every input element (they all share one
    normalizing sum), so backward can't be a simple elementwise product.
    The full vector-Jacobian product, reducing along the last axis, is:

        dL/dx_i = output_i * (grad_output_i - sum_j(grad_output_j * output_j))

    Returns an array the same shape as grad_output/output.
    """
    pass
