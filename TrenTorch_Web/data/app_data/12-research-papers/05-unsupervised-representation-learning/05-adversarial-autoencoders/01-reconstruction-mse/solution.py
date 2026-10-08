import numpy as np


def reconstruction_mse(x, x_hat):
    x = np.asarray(x, dtype=float)
    x_hat = np.asarray(x_hat, dtype=float)
    return float(np.mean((x - x_hat) ** 2))
