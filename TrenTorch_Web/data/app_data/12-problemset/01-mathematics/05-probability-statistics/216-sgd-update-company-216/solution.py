import numpy as np

def solve(theta,grad,lr): return np.asarray(theta)-lr*np.asarray(grad)
