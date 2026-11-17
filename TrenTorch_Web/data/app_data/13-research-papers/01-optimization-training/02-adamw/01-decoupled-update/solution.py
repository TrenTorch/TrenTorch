import numpy as np


def adamw_update(w, m_hat, v_hat, lr, wd, eps):
    return w - lr * (m_hat / (np.sqrt(v_hat) + eps) + wd * w)
