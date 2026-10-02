import numpy as np


def lu_decompose(A):
    n = A.shape[0]
    U = A.astype(float).copy()
    L = np.eye(n)

    for j in range(n):
        for i in range(j + 1, n):
            multiplier = U[i, j] / U[j, j]
            L[i, j] = multiplier
            U[i] = U[i] - multiplier * U[j]

    return L, U
