import numpy as np

def solve(p):
    p=np.asarray(p,dtype=float)
    q=p[p>0]
    return float(-np.sum(q*np.log2(q)))
