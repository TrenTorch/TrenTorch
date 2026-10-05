import numpy as np

def solve(x):
    x=np.asarray(x,dtype=float)
    lo,hi=np.min(x),np.max(x)
    if hi==lo: return np.zeros_like(x)
    return (x-lo)/(hi-lo)
