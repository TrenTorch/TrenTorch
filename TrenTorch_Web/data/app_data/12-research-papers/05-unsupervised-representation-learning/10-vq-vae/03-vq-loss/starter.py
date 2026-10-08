import numpy as np


def vq_loss(z, e, beta):
    """
    z: encoder outputs, shape (n, d)
    e: the chosen code vectors for those outputs, shape (n, d)
    beta: commitment weight

    Returns:
        The codebook term plus beta times the commitment term, as a float.
        Forward values match; the stop-gradient placement is what differs.
    """
    # TODO: Compute the squared distance between encoder outputs and codes, weighted per the paper (see Theory).
    pass
