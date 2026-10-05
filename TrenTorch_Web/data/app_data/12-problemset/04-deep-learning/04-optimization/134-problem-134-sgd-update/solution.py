import numpy as np

def solve(w, grad, lr):
    """One SGD step subtracts learning-rate times gradient from each parameter."""
    return np.asarray(w)-lr*np.asarray(grad)
