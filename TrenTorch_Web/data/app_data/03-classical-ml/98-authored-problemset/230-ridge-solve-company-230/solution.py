import numpy as np

def solve(X,y,lam):
    X=np.asarray(X,float); y=np.asarray(y,float); d=X.shape[1]; A=X.T@X+lam*np.eye(d); return np.linalg.solve(A,X.T@y)
