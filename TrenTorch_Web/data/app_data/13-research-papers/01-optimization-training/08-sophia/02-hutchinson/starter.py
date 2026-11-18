import numpy as np


def hutchinson_estimate(Hu, u):
    """
    Hu: the Hessian-vector product H u, shape (d,)
    u: the random probe vector with entries +1 or -1, shape (d,)

    Returns:
        The element-wise product u * (H u), an unbiased estimate of the Hessian diagonal.
    """
    # TODO: Multiply the Hessian-vector product by the probe element-wise (see Theory).
    pass
