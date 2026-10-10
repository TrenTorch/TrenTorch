import numpy as np

def solve(w,lam):
        w=np.asarray(w,float); return float(lam*np.sum(w*w))
