import math


def online_softmax_merge(m1, l1, m2, l2):
    """
    m1, l1: running max and running sum of exp(score - max) for the first block
    m2, l2: the same statistics for the second block

    Returns:
        (m, l) for the union of the two blocks, with l equal to sum of exp(score - m).
    """
    # TODO: Take the larger max and rescale both sums to it (see Theory).
    pass
