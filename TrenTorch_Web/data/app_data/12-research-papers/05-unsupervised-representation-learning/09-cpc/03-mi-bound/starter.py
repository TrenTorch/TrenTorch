import math


def mi_lower_bound(n_candidates, loss):
    """
    n_candidates: number of candidate futures in the contrastive set
    loss: the CPC loss value on that set

    Returns:
        The mutual information lower bound log(N) - loss, as a float.
    """
    # TODO: Subtract the loss from log of the candidate count (see Theory).
    pass
