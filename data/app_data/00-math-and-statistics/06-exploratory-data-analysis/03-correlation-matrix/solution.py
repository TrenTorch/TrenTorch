import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

correlation = load_solution("00-math-and-statistics/03-probability/03-covariance-correlation").correlation


def correlation_matrix(x: np.ndarray) -> np.ndarray:
    num_features = x.shape[1]
    result = np.eye(num_features)
    for i in range(num_features):
        for j in range(i + 1, num_features):
            value = correlation(x[:, i], x[:, j])
            result[i, j] = value
            result[j, i] = value
    return result


def most_correlated_pair(corr_matrix: np.ndarray) -> tuple[int, int]:
    n = corr_matrix.shape[0]
    off_diagonal = corr_matrix.copy()
    np.fill_diagonal(off_diagonal, 0.0)
    flat_index = np.argmax(np.abs(off_diagonal))
    return tuple(np.unravel_index(flat_index, (n, n)))
