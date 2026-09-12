import numpy as np


def mse_loss_forward(input: np.ndarray, target: np.ndarray, reduction: str = "mean"):
    """
    Mirrors torch.nn.functional.mse_loss(input, target, reduction=reduction).

    reduction:
        "mean": average squared error over every element (the default).
        "sum":  total squared error, no averaging.
        "none": the per-element squared error itself, no reduction at all.
    """
    pass


def mse_loss_backward(
    input: np.ndarray, target: np.ndarray, reduction: str = "mean", grad_output=1.0
) -> np.ndarray:
    """
    dL/d_input for MSE. The unreduced per-element gradient is always
    2*(input - target); "mean" divides that by the element count (since
    the forward pass divided the sum by that same count), "sum" and
    "none" leave it as is.

    grad_output: the upstream gradient flowing in from whatever used
    this loss's output (almost always 1.0, since a loss is usually the
    very end of the graph, but kept general to chain correctly either way).
    """
    pass
