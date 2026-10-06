import numpy as np

def solve(X,y,q,k):
        X=np.asarray(X,float); q=np.asarray(q,float); d=np.sum((X-q)**2,axis=1); return float(np.mean(np.asarray(y)[np.argsort(d)[:k]]))
