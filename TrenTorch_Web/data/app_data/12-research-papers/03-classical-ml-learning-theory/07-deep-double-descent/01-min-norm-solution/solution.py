import numpy as np


def min_norm_solution(X, y):
    return np.linalg.pinv(X) @ y
