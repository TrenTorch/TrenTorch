import numpy as np


def sophia_step(m, h, gamma, eps):
    """
    m: momentum, shape (d,); h: diagonal Hessian estimate, shape (d,)
    gamma: scaling of the Hessian; eps: floor on the denominator

    Returns:
        The clipped per-coordinate step clip(m / max(gamma * h, eps), -1, 1).
    """
    # TODO: Divide the momentum by the floored scaled Hessian, then clip each entry to [-1, 1] (see Theory).
    pass
