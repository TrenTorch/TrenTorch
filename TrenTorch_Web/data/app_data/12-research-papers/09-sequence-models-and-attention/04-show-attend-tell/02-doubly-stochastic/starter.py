import numpy as np


def doubly_stochastic_penalty(alpha):
    """
    alpha: attention matrix, shape (T, L), row t the weights over locations at word t

    Returns:
        The penalty sum_i (1 - sum_t alpha[t, i])^2, which pushes every location to be attended to about once.
    """
    # TODO: Sum each location's attention over the words, then penalize its distance from one (see Theory).
    pass
