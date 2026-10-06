import numpy as np

def solve(X,dY,W):
        X,dY=np.asarray(X),np.asarray(dY); return dY@W.T, X.T@dY, dY.sum(0)
