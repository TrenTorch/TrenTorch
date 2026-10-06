import numpy as np

def solve(x):
        X=np.asarray(X,float); lo=X.min(0); hi=X.max(0); span=hi-lo
        return np.divide(X-lo,span,out=np.zeros_like(X),where=span!=0)
