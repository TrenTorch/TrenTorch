import numpy as np

def solve(X):
    X=np.asarray(X,float)
    return ((X[:,None,:]-X[None,:,:])**2).sum(axis=2)
