import numpy as np

def solve(X):
    X=np.asarray(X,dtype=float).copy()
    for j in range(X.shape[1]):
        col=X[:,j]; m=np.nanmean(col)
        col[np.isnan(col)]=m
    return X
