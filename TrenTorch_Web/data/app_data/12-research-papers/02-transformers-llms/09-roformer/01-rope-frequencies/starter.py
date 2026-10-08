import numpy as np


def rope_frequencies(d, base=10000.0):
    """
    d: feature dimension (even)
    base: the frequency base, 10000 by default

    Returns:
        theta_i = base ** (-2i / d) for i = 0 .. d/2 - 1, shape (d/2,).
    """
    # TODO: Compute the d/2 rotary frequencies from Theory.
    pass
