import numpy as np


def dirichlet_mix(P, noise, eps):
    """
    P: the network's prior over root moves, shape (A,)
    noise: a sample from a Dirichlet distribution, shape (A,)
    eps: how much noise to mix in, in [0, 1]

    Returns:
        (1 - eps) * P + eps * noise, the root prior used for exploration.
    """
    # TODO: Blend the prior with the Dirichlet noise (see Theory).
    pass
