import numpy as np

def solve(y_true, y_pred):
    return float(np.mean(np.asarray(y_true) == np.asarray(y_pred)))
