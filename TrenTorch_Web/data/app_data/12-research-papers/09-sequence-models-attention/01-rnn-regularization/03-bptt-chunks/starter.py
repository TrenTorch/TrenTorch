import math


def bptt_chunks(T, bptt):
    """
    T: length of the training sequence
    bptt: truncation length for backpropagation through time

    Returns:
        The number of truncated segments needed to cover T steps, rounding up.
    """
    # TODO: Divide T by the truncation length and round up (see Theory).
    pass
