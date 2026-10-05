import numpy as np

def solve(z,y):
    z=np.asarray(z,float); y=np.asarray(y,float)
    return float(np.mean(np.maximum(z,0)-z*y+np.log1p(np.exp(-np.abs(z)))))
