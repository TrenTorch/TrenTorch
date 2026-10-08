import numpy as np


def lamb_direction(m_hat, v_hat, w, wd, eps):
    """
    m_hat, v_hat: bias-corrected Adam moments; w: layer weights
    wd: weight decay; eps: numerical floor

    Returns:
        The Adam direction with decay added, r = m_hat / (sqrt(v_hat) + eps) + wd * w.
    """
    # TODO: Form the Adam ratio and add the decay term (see Theory).
    pass
