import numpy as np


def causal_mask(n):
    """
    n: sequence length

    Returns:
        An (n, n) boolean matrix where entry [i, j] is True when position i may
        attend to position j, i.e. j <= i.
    """
    # TODO: Build the lower-triangular boolean matrix (see Theory).
    pass
