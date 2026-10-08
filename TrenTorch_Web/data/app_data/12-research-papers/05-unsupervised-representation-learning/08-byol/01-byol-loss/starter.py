import numpy as np


def byol_loss(p, z):
    """
    p: prediction from the online network's predictor, shape (d,)
    z: projection from the target network, shape (d,)

    Returns:
        2 - 2 * cos(p, z), the normalized regression loss, as a float.
    """
    # TODO: Compute the cosine similarity of p and z and return 2 - 2 cos (see Theory).
    pass
