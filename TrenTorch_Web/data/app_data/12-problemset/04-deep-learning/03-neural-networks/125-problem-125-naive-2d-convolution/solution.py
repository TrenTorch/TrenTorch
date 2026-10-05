import numpy as np

def solve(X, K):
    X = np.asarray(X, dtype=float)
    K = np.asarray(K, dtype=float)
    height, width = X.shape
    kernel_height, kernel_width = K.shape
    output = np.empty((height - kernel_height + 1, width - kernel_width + 1), dtype=float)
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            output[i, j] = np.sum(X[i:i + kernel_height, j:j + kernel_width] * K)
    return output
