import numpy as np

def solve(x):
    x=np.asarray(x,float); m=x.mean(); s=x.std()
    return np.zeros_like(x) if s==0 else (x-m)/s
