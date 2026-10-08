import numpy as np


def lora_delta(A, B, alpha, r):
    """
    A: down-projection, shape (r, d_in)
    B: up-projection, shape (d_out, r), initialized to zero in the paper
    alpha: scaling constant
    r: rank of the update

    Returns:
        The weight update (alpha / r) * B A, shape (d_out, d_in).
    """
    # TODO: Multiply B by A and apply the alpha / r scale (see Theory).
    pass
