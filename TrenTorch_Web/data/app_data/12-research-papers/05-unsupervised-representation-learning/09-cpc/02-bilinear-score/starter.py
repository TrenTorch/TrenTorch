import numpy as np


def bilinear_score(c, W, z):
    """
    c: context vector, shape (d_c,)
    W: learned matrix, shape (d_c, d_z)
    z: latent vector, shape (d_z,)

    Returns:
        The compatibility score c^T W z, as a float.
    """
    # TODO: Compute the bilinear form c W z (see Theory).
    pass
