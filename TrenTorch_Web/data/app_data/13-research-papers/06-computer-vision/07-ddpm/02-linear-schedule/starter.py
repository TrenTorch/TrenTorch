import numpy as np


def alpha_bars(T, b0, b1):
    """
    T: number of diffusion steps
    b0, b1: noise variance at the first and last step

    Returns:
        The cumulative signal fractions alpha_bar_t, shape (T,), from a linear beta schedule.
    """
    # TODO: Build the linear beta schedule and take its cumulative product of (1 - beta) (see Theory).
    pass
