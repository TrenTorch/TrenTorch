import numpy as np


def quantize_symmetric(x, bits):
    """
    x: weight values to quantize
    bits: number of bits per integer (at least 2)

    Returns:
        (q, scale): integer codes in [-qmax, qmax] with qmax = 2**(bits-1) - 1, and the scale that maps them back.
    """
    # TODO: Choose a scale from the largest magnitude, then round and clip the codes (see Theory).
    pass
