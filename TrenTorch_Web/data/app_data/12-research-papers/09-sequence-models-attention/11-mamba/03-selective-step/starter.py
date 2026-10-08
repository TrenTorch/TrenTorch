import numpy as np


def selective_step(delta_raw):
    """
    delta_raw: unconstrained output of a linear layer applied to the input

    Returns:
        A positive step size softplus(delta_raw), computed stably.
    """
    # TODO: Map the unconstrained value to a positive step with softplus (see Theory).
    pass
