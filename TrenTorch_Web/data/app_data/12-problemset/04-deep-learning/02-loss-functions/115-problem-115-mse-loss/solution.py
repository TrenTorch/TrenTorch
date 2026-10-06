import numpy as np

def solve(y,pred):
        return float(np.mean((np.asarray(y)-np.asarray(pred))**2))
