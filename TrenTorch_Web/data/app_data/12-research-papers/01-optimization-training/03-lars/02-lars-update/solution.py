import numpy as np


def lars_update(w, g, lr, eta, wd):
    local = eta * np.linalg.norm(w) / (np.linalg.norm(g) + wd * np.linalg.norm(w))
    return w - lr * local * (g + wd * w)
