import numpy as np

def solve(X):
    X=np.asarray(X,float)
    return X-X.mean(axis=0)
