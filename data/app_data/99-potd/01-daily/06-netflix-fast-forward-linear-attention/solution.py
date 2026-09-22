import numpy as np


def feature_map(x: np.ndarray) -> np.ndarray:
    return np.maximum(x, 0.0) + 1.0


def linear_attention_row_sums(Q: np.ndarray, K: np.ndarray, V: np.ndarray) -> np.ndarray:
    q_prime = feature_map(Q)
    k_prime = feature_map(K)

    m = k_prime.T @ V
    z = k_prime.sum(axis=0)

    # sum_j (Q'M)[i, j] == Q'[i] . (row sums of M), so the (N, d) numerator
    # never has to exist: only an (N,) vector does.
    numerator = q_prime @ m.sum(axis=1)
    denominator = q_prime @ z
    return numerator / denominator
