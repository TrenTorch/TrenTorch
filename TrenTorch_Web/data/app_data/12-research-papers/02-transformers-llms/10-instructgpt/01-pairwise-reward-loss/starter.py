import numpy as np


def pairwise_reward_loss(r_chosen, r_rejected):
    """
    r_chosen: reward model score for the preferred response
    r_rejected: reward model score for the dispreferred response

    Returns:
        -log(sigmoid(r_chosen - r_rejected)), computed stably.
    """
    # TODO: Compute -log sigmoid of the reward margin (see Theory).
    pass
