import math


def relative_step(t):
    """
    t: step count starting at 1

    Returns:
        The relative step size min(0.01, 1 / sqrt(t)) used when no external learning rate is given.
    """
    # TODO: Take the smaller of 0.01 and one over the square root of t (see Theory).
    pass
