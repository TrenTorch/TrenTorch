import numpy as np

def solve(X,w):
    X=np.asarray(X,float); w=np.asarray(w,float); p=w/w.sum(); mu=(p[:,None]*X).sum(axis=0); Z=X-mu; return (Z*p[:,None]).T@Z
