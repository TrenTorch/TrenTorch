import numpy as np


def adamw_update(w, m_hat, v_hat, lr, wd, eps):
    """
    w: current weights
    m_hat, v_hat: bias-corrected first and second moment estimates
    lr: learning rate; wd: decoupled weight decay; eps: numerical floor

    Returns:
        The updated weights, with weight decay applied directly to w rather than through the gradient.
    """
    # TODO: Take the Adam step, then subtract the decay term lr * wd * w (see Theory).
    pass
