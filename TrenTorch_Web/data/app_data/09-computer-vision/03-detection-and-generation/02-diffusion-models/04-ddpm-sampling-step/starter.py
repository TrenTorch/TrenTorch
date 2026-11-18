import numpy as np


def ddpm_step(x_t: np.ndarray, eps_pred: np.ndarray, t: int, betas: np.ndarray, alpha_bars: np.ndarray, z: np.ndarray) -> np.ndarray:
    """One ancestral sampling step x_t -> x_{t-1} (no noise when t == 0)."""
    # TODO
    pass
