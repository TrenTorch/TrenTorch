import numpy as np


def nt_xent_anchor(sim_pos, sims_neg, tau):
    """
    sim_pos: similarity between the anchor and its positive view
    sims_neg: similarities between the anchor and every other sample in the batch
    tau: temperature (positive)

    Returns:
        -log(exp(sim_pos / tau) / (exp(sim_pos / tau) + sum exp(sims_neg / tau))), as a float.
    """
    # TODO: Compute the softmax log-loss of the positive among all candidates (see Theory).
    pass
