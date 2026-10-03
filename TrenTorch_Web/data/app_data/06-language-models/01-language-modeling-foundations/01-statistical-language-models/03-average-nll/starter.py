import numpy as np


def average_nll(words: list[str], probs: np.ndarray, itos: list[str]) -> float:
    """
    Mean negative log-probability (natural log) of every adjacent pair of
    the words, each wrapped as '.' + word + '.'.
    """
    # TODO: Collect row/column indices of all pairs, look up probs, average.
    pass
