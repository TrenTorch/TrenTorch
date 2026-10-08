import numpy as np


def memory_output(p, outputs):
    return np.asarray(p, dtype=float) @ np.asarray(outputs, dtype=float)
