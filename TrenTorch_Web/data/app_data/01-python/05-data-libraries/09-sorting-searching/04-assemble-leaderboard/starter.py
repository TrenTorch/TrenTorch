import numpy as np


def top_k(scores: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k highest scores, highest first; ties go to the lower index."""
    # TODO: Stable descending order, first k.
    pass


def competition_ranks(scores: np.ndarray) -> np.ndarray:
    """
    1-based rank of every player, highest score = 1. Equal scores share the best
    rank and the next rank is skipped: [90, 80, 80, 70] -> [1, 2, 2, 4].
    """
    # TODO: One plus the number of strictly higher scores.
    pass


def kth_largest(scores: np.ndarray, k: int):
    """The k-th largest value (k = 1 is the maximum) without sorting the whole array."""
    # TODO: Use a partial sort.
    pass


def percentile_rank(scores: np.ndarray) -> np.ndarray:
    """For each score, the fraction of all scores that are strictly smaller."""
    # TODO: Count the smaller scores with a binary search.
    pass
