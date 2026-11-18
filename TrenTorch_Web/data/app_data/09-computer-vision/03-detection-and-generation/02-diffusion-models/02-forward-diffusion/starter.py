import numpy as np


def q_sample(x0: np.ndarray, t: int, alpha_bars: np.ndarray, noise: np.ndarray) -> np.ndarray:
    """Noisy sample x_t = sqrt(ab[t]) * x0 + sqrt(1 - ab[t]) * noise."""
    # TODO
    pass


def snr(alpha_bars: np.ndarray) -> np.ndarray:
    """Signal-to-noise ratio ab / (1 - ab) at every step."""
    # TODO
    pass
