import numpy as np


def adamax_step(
    param,
    grad,
    m,
    u,
    lr,
    beta1,
    beta2,
    eps,
):
    """Apply one Adamax optimization step.

    Args:
        param: Parameter array.
        grad: Gradient array with the same shape as param.
        m: First moment (moving average of gradients).
        u: Infinity norm (max absolute gradient seen).
        lr: Positive learning rate.
        beta1: Decay factor for first moment, in [0, 1).
        beta2: Decay factor for infinity norm, in [0, 1).
        eps: Positive numerical stability constant.

    Returns:
        A tuple (new_param, new_m, new_u).

    Raises:
        ValueError: If input shapes do not match, lr is not positive,
            beta1 or beta2 are outside [0, 1), or eps is not positive.
    """
    if (
        param.shape != grad.shape
        or param.shape != m.shape
        or param.shape != u.shape
    ):
        raise ValueError(
            "param, grad, m, and u must have the same shape"
        )

    if lr <= 0:
        raise ValueError("lr must be positive")

    if not (0 <= beta1 < 1):
        raise ValueError("beta1 must be in [0, 1)")

    if not (0 <= beta2 < 1):
        raise ValueError("beta2 must be in [0, 1)")

    if eps <= 0:
        raise ValueError("eps must be positive")

    m_new = beta1 * m + (1 - beta1) * grad

    u_new = np.maximum(beta2 * u, np.abs(grad))

    param_new = param - lr * m_new / (u_new + eps)

    return param_new, m_new, u_new
