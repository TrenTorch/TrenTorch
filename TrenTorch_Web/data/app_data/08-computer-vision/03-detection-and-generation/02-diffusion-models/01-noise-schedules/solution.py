import numpy as np


def linear_betas(T, beta_start, beta_end):
    return np.linspace(beta_start, beta_end, T)


def alpha_bars(betas):
    return np.cumprod(1.0 - np.asarray(betas, dtype=float))


def cosine_alpha_bars(T, s=0.008):
    def f(u):
        return np.cos(((u / T) + s) / (1 + s) * np.pi / 2) ** 2
    return f(np.arange(1, T + 1)) / f(0)
