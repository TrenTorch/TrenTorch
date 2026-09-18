import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

correlation = load_solution("00-math-and-statistics/03-probability/03-covariance-correlation").correlation


def correlation_matrix(x: np.ndarray) -> np.ndarray:
    """
    x is (num_samples, num_features). Returns a (num_features,
    num_features) matrix where entry [i, j] is the correlation
    (03-probability/03-covariance-correlation's `correlation`, already
    provided above) between feature column i and feature column j.

    The diagonal is always 1.0 (every feature correlates perfectly
    with itself), and the matrix is symmetric (corr(i, j) == corr(j, i)).
    """
    pass


def most_correlated_pair(corr_matrix: np.ndarray) -> tuple[int, int]:
    """
    Given a correlation matrix, returns the (row, col) index of the
    single most correlated pair of DIFFERENT features (excluding the
    diagonal, which is always a trivial 1.0), by absolute value (a
    strong NEGATIVE correlation counts too).
    """
    pass
