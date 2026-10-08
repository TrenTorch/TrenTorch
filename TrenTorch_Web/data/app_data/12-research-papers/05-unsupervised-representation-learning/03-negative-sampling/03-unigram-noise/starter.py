import numpy as np


def unigram_noise(counts, power=0.75):
    """
    counts: word counts in the corpus, shape (V,)
    power: exponent that flattens the distribution (0.75 in the paper)

    Returns:
        The noise distribution proportional to counts ** power, summing to 1.
    """
    # TODO: Raise the counts to the power and normalize them (see Theory).
    pass
