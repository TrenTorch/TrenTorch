import numpy as np


def matmul_from_scratch(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    m, k = a.shape
    k2, n = b.shape
    if k != k2:
        raise ValueError(f"inner dimensions must match, got {a.shape} and {b.shape}")

    result = np.zeros((m, n), dtype=np.result_type(a, b))
    for i in range(m):
        for j in range(n):
            result[i, j] = np.sum(a[i, :] * b[:, j])
    return result
