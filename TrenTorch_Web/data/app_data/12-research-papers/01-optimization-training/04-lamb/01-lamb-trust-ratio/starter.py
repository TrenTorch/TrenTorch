import numpy as np


def lamb_trust_ratio(w, r):
    """
    w: layer weights; r: the Adam-style direction for the layer, including decay

    Returns:
        The ratio ||w|| / ||r|| as a float.
    """
    # TODO: Divide the weight norm by the norm of the update direction (see Theory).
    pass
