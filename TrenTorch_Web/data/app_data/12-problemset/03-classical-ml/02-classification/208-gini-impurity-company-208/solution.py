import numpy as np

def solve(y):
    y=np.asarray(y)
    if len(y)==0: return 0.0
    p=np.mean(y==1)
    return float(1-p*p-(1-p)*(1-p))
