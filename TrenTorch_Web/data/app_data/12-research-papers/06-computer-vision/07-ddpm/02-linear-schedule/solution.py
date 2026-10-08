import numpy as np


def alpha_bars(T, b0, b1):
    betas = np.linspace(b0, b1, T)
    return np.cumprod(1 - betas)
