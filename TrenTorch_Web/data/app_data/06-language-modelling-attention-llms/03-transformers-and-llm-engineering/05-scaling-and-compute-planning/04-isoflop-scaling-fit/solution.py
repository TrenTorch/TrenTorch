import numpy as np


def isoflop_optimum(params, losses):
    a, b, _ = np.polyfit(np.log(np.asarray(params, float)), np.asarray(losses, float), 2)
    if a <= 0:
        raise ValueError("loss curve has no interior minimum")
    return float(np.exp(-b / (2 * a)))


def fit_power_law(x, y):
    b, intercept = np.polyfit(np.log(np.asarray(x, float)), np.log(np.asarray(y, float)), 1)
    return float(np.exp(intercept)), float(b)
