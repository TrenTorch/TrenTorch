import numpy as np


def jsd_estimate(pos, neg):
    """
    pos: discriminator scores for matched (positive) pairs
    neg: discriminator scores for mismatched (negative) pairs

    Returns:
        E_pos[-softplus(-s)] - E_neg[softplus(s)], the Jensen-Shannon mutual information estimate.
    """
    # TODO: Apply softplus to the positive and negative scores and combine their means (see Theory).
    pass
