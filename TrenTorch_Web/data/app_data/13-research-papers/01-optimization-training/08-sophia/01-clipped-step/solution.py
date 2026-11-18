import numpy as np


def sophia_step(m, h, gamma, eps):
    return np.clip(m / np.maximum(gamma * h, eps), -1.0, 1.0)
