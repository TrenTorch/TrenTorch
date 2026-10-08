import numpy as np


def dropout_backward(grad_out, keep_mask, p):
    """
    grad_out: gradient of the loss with respect to the dropout output
    keep_mask: the same 0/1 mask used in the forward pass
    p: the drop probability used in the forward pass

    Returns:
        The gradient with respect to the dropout input, from Theory.
    """
    # TODO: Gate the gradient by the mask and rescale by 1 / (1 - p).
    pass
