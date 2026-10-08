import numpy as np


def lamb_direction(m_hat, v_hat, w, wd, eps):
    return m_hat / (np.sqrt(v_hat) + eps) + wd * w
