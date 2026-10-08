import numpy as np


def unpool_with_switches(pooled, switches, size):
    """
    pooled: pooled values, one per window
    switches: the recorded offset of each window's maximum
    size: pooling window size

    Returns:
        A signal of length len(pooled) * size with each value placed at its switch, zeros elsewhere.
    """
    # TODO: Place each pooled value at its switch position inside its window (see Theory).
    pass
