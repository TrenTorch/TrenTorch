import numpy as np

def solve(X,mask):
    X=np.asarray(X,float); m=np.asarray(mask).astype(bool)
    if m.sum()==0: return np.zeros(X.shape[1])
    return X[m].mean(axis=0)
