import math

import numpy as np


def sturges_bins(n: int) -> int:
    return int(math.ceil(math.log2(n)) + 1)


def freedman_diaconis_bins(x: np.ndarray) -> int:
    x = np.asarray(x, dtype=float)
    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1
    if iqr == 0.0:
        return sturges_bins(len(x))
    width = 2.0 * iqr / len(x) ** (1.0 / 3.0)
    return max(1, int(math.ceil((x.max() - x.min()) / width)))


def bin_edges(x: np.ndarray, n_bins: int) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return np.linspace(x.min(), x.max(), n_bins + 1)


def histogram_counts(x: np.ndarray, edges: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    edges = np.asarray(edges, dtype=float)
    n_bins = len(edges) - 1
    inside = x[(x >= edges[0]) & (x <= edges[-1])]
    index = np.searchsorted(edges, inside, side="right") - 1
    index = np.minimum(index, n_bins - 1)
    return np.bincount(index, minlength=n_bins).astype(int)
