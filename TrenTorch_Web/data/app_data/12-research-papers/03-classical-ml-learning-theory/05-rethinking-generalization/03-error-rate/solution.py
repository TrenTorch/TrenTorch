import numpy as np


def error_rate(pred, y):
    return float(np.mean(np.asarray(pred) != np.asarray(y)))
