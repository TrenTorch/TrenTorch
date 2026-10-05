import numpy as np

def solve(scores,V):
    s=np.asarray(scores,float); V=np.asarray(V,float)
    p=np.exp(s-s.max()); p=p/p.sum()
    return p@V
