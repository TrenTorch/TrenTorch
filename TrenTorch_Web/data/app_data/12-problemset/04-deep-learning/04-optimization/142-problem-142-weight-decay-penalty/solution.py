import numpy as np

def solve(w, lam):
    """The L2 weight-decay penalty returned here is lambda times the sum of squared weights."""
    w=np.asarray(w,dtype=float); return float(lam*np.sum(w*w))
