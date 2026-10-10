import numpy as np

def solve(w,grad,lr):
        return np.asarray(w)-lr*np.asarray(grad)
