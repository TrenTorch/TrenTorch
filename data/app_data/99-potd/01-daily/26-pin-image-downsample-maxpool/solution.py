import numpy as np


def max_pool_strided(matrix: np.ndarray, k: int, s: int) -> np.ndarray:
    H, W = matrix.shape
    out_h = (H - k) // s + 1
    out_w = (W - k) // s + 1

    output = np.empty((out_h, out_w), dtype=matrix.dtype)
    for i in range(out_h):
        row = i * s
        for j in range(out_w):
            col = j * s
            output[i, j] = matrix[row : row + k, col : col + k].max()
    return output
