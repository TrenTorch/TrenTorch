import numpy as np


def friedman_statistic(scores: np.ndarray) -> float:
    """
    chi2_F for an (N, k) score matrix (higher is better), ranks 1 = best with
    average ranks for ties, and chi2 = 12 / (N k (k + 1)) * sum_j R_j^2 - 3 N (k + 1),
    where R_j is the rank sum of column j. Raise ValueError for bad shapes or
    non-finite scores.
    """
    pass
