import numpy as np


def act_output(outs, halts):
    """
    outs: the output of each computation step, length N
    halts: halting probabilities for the steps, length N; the last entry gets the remainder

    Returns:
        The halting-weighted average of the step outputs, as a float.
    """
    # TODO: Weight each step's output by its halting probability, with the remainder on the last step (see Theory).
    pass
