import numpy as np


def visit_distribution(counts, tau):
    """
    counts: visit counts of each root move after search, shape (A,), all positive
    tau: temperature (positive); small tau is close to greedy

    Returns:
        The policy target pi proportional to counts ** (1 / tau), normalized to sum to 1.
    """
    # TODO: Raise the counts to the power 1 / tau and normalize (see Theory).
    pass
