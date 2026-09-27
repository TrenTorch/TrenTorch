import numpy as np


def gaussian_eliminate(A, b):
    n = A.shape[0]
    U = A.astype(float).copy()
    c = b.astype(float).copy()

    for j in range(n):
        for i in range(j + 1, n):
            multiplier = U[i, j] / U[j, j]
            U[i] = U[i] - multiplier * U[j]
            c[i] = c[i] - multiplier * c[j]

    return U, c


def back_substitute(U, c):
    n = U.shape[0]
    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        x[i] = (c[i] - U[i, i + 1 :] @ x[i + 1 :]) / U[i, i]

    return x
