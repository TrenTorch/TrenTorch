import numpy as np


def topic_conditional(
    doc_counts: np.ndarray,
    topic_word: np.ndarray,
    topic_totals: np.ndarray,
    alpha: float,
    beta: float,
    word: int,
) -> np.ndarray:
    """
    Normalized p(z = k | rest) for one token of `word`, with the token already
    removed from the counts. Raise ValueError for shape mismatches, nonpositive
    alpha or beta, negative counts, or an out-of-range word index.
    """
    pass
