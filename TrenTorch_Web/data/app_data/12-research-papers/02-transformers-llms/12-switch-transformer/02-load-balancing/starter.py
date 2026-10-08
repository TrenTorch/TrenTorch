import numpy as np


def load_balancing_loss(expert_index, probs, n_experts):
    """
    expert_index: the expert chosen for each token, shape (T,)
    probs: router softmax probabilities, shape (T, E)
    n_experts: number of experts E

    Returns:
        The auxiliary loss E * sum_i f_i * P_i, where f_i is the fraction of tokens sent to
        expert i and P_i is the mean router probability for expert i.
    """
    # TODO: Compute f_i and P_i, then the scaled dot product (see Theory).
    pass
