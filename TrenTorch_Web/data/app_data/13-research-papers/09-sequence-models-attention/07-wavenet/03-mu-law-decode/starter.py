import numpy as np


def mu_law_decode(y, mu=255):
    """
    y: companded values in [-1, 1]
    mu: companding parameter (255 in WaveNet)

    Returns:
        The inverse mu-law expansion, sign(y) * ((1 + mu)^|y| - 1) / mu.
    """
    # TODO: Invert the mu-law compression element-wise (see Theory).
    pass
