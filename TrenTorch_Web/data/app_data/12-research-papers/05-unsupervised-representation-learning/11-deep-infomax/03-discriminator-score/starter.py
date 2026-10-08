import numpy as np


def discriminator_score(local, global_vec, W):
    """
    local: a local feature vector, shape (d_l,)
    global_vec: a global summary vector, shape (d_g,)
    W: learned matrix, shape (d_l, d_g)

    Returns:
        The score local^T W global_vec, as a float.
    """
    # TODO: Compute the bilinear score between the local and global vectors (see Theory).
    pass
