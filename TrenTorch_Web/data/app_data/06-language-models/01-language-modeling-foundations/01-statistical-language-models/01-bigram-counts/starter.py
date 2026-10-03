import numpy as np


def bigram_counts(words: list[str]) -> tuple[np.ndarray, list[str]]:
    """
    Returns (counts, itos). `itos` is ['.'] plus the sorted distinct
    characters of all words. counts[i, j] is how often itos[j] directly
    followed itos[i] when every word is wrapped as '.' + word + '.'.
    """
    # TODO: Build itos and a symbol -> index map.
    # TODO: Walk the adjacent pairs of each wrapped word and count them.
    pass
