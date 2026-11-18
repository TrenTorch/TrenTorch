import numpy as np

def solve(X,C):
    X=np.asarray(X,float); C=np.asarray(C,float)
    d=((X[:,None,:]-C[None,:,:])**2).sum(axis=2)
    return np.argmin(d,axis=1)
