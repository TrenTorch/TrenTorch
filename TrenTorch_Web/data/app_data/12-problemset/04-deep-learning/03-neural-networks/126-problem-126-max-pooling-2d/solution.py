import numpy as np

def solve(X, k, s=1):
    """Max pooling returns the maximum value in each k-by-k window positioned every s cells."""
    X=np.asarray(X,dtype=float); out=np.empty(((X.shape[0]-k)//s+1,(X.shape[1]-k)//s+1));
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i,j]=np.max(X[i*s:i*s+k,j*s:j*s+k])
    return out
