import numpy as np

def solve(logits):
    x=np.asarray(logits,dtype=float)
    z=x-np.max(x)
    e=np.exp(z)
    return e/e.sum()
