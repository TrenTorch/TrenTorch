import numpy as np


def ddim_step(x_t: np.ndarray, eps_pred: np.ndarray, t: int, t_prev: int, alpha_bars: np.ndarray) -> np.ndarray:
    """Deterministic DDIM update from noise level t to t_prev (t_prev = -1 means fully clean)."""
    # TODO
    pass
