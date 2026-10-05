import numpy as np


def causal_conv1d(x, w):
    """
    x: input sequence, shape (T,)
    w: kernel, where w[j] multiplies the input j steps in the past

    Returns:
        The causal convolution out[t] = sum_j w[j] * x[t - j], with zeros before the start. Shape (T,).
    """
    # TODO: Accumulate each kernel tap times the input j steps back, treating the past before t=0 as zero (see Theory).
    pass
