import math


def pyramid_length(T, layers):
    """
    T: number of input acoustic frames
    layers: number of pyramidal layers, each halving the time resolution

    Returns:
        The number of frames after the pyramid, ceil(T / 2^layers).
    """
    # TODO: Halve the sequence length once per pyramidal layer, rounding up (see Theory).
    pass
