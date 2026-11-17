import numpy as np


def swiglu(x, W, V):
    """
    x: input activations, shape (T, d)
    W: gate projection, shape (d, h)
    V: up projection, shape (d, h)

    Returns:
        silu(x W) * (x V), shape (T, h), where silu(z) = z * sigmoid(z).
    """
    # TODO: Compute the SiLU-gated product of the two projections (see Theory).
    pass
