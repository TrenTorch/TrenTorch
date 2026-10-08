import numpy as np


def finalize_output(acc, l):
    """
    acc: unnormalized output accumulator, shape (n, d)
    l: running softmax denominator per query row, shape (n,)

    Returns:
        The attention output acc / l, normalized once at the end.
    """
    # TODO: Divide each row of the accumulator by its softmax denominator (see Theory).
    pass
