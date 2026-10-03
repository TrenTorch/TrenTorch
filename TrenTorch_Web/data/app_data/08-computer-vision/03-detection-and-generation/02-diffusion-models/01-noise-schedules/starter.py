import numpy as np


def linear_betas(T: int, beta_start: float, beta_end: float) -> np.ndarray:
    """T evenly spaced noise variances."""
    # TODO
    pass


def alpha_bars(betas: np.ndarray) -> np.ndarray:
    """Cumulative product of (1 - beta)."""
    # TODO
    pass


def cosine_alpha_bars(T: int, s: float = 0.008) -> np.ndarray:
    """alpha_bar[t] = f(t + 1) / f(0) for t = 0..T-1 with f the squared cosine."""
    # TODO
    pass
