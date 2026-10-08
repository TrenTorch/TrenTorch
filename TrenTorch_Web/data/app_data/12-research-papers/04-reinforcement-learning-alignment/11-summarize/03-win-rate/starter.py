import numpy as np


def win_rate(a, b):
    """
    a: scores of system A on each prompt, shape (N,)
    b: scores of system B on the same prompts, shape (N,)

    Returns:
        The fraction of prompts where A wins, with ties counted as half a win.
    """
    # TODO: Count wins for A, count half of the ties, and divide by the number of prompts (see Theory).
    pass
