import numpy as np


def char_nll(logp, targets):
    """
    logp: log-probabilities over characters at each output step, shape (S, V)
    targets: correct character index at each step, shape (S,)

    Returns:
        The summed negative log-likelihood of the transcript, as a float.
    """
    # TODO: Sum the negative log-probability of each correct character (see Theory).
    pass
