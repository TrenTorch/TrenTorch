import numpy as np


def q_sample(x0, t, alpha_bars, noise):
    ab = alpha_bars[t]
    return np.sqrt(ab) * np.asarray(x0, dtype=float) + np.sqrt(1.0 - ab) * np.asarray(noise, dtype=float)


def snr(alpha_bars):
    ab = np.asarray(alpha_bars, dtype=float)
    return ab / (1.0 - ab)
