import numpy as np


def entropy(p):
    """
    p: a probability distribution over actions, shape (A,), summing to 1

    Returns:
        The Shannon entropy -sum p log p, as a float. Zero-probability entries contribute 0.
    """
    # TODO: Sum -p log p over the actions, treating 0 log 0 as 0 (see Theory).
    pass
