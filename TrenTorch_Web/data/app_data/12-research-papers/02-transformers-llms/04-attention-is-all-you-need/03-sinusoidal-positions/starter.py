import numpy as np


def sinusoidal_positional_encoding(T, d):
    """
    T: sequence length
    d: model dimension (even)

    Returns:
        A (T, d) array with PE[pos, 2i] = sin(pos / 10000^(2i/d)) and
        PE[pos, 2i+1] = cos(pos / 10000^(2i/d)).
    """
    # TODO: Fill even columns with sin and odd columns with cos (see Theory).
    pass
