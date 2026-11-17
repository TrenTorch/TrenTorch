import math


def subsample_keep_prob(freq, t):
    """
    freq: relative frequency of the word in the corpus, in (0, 1]
    t: subsampling threshold, e.g. 1e-5

    Returns:
        The probability of keeping an occurrence of the word, min(1, sqrt(t / freq)).
    """
    # TODO: Compute sqrt(t / freq) and cap it at 1 (see Theory).
    pass
