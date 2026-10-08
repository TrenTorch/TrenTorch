import numpy as np


def dpo_loss(logit):
    """
    logit: the DPO implicit reward margin, scalar or array

    Returns:
        -log(sigmoid(logit)) = log(1 + exp(-logit)), computed stably.
    """
    # TODO: Compute the negative log-sigmoid of the margin in a numerically stable way (see Theory).
    pass
