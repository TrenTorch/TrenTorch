import numpy as np


def allreduce_sum(parts):
    """
    parts: one partial result per device, all of the same shape

    Returns:
        The element-wise sum of the partial results, which every device ends up holding.
    """
    # TODO: Sum the per-device partial results element-wise (see Theory).
    pass
