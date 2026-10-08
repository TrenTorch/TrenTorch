import numpy as np


def masked_lm_loss(log_probs, targets, mask):
    """
    log_probs: log-probabilities over the vocabulary at each position, shape (T, V)
    targets: the original token index at each position, shape (T,)
    mask: boolean array, True where the token was selected for prediction

    Returns:
        The mean negative log-likelihood over masked positions only, or 0.0 if none are masked.
    """
    # TODO: Average -log p(target) over the positions where mask is True (see Theory).
    pass
