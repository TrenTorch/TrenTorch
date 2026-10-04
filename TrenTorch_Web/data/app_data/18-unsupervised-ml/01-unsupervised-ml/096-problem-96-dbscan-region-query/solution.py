import numpy as np

def solve(X,i,eps):
        X=np.asarray(X,float); d=np.sum((X-X[i])**2,axis=1); return np.where(d<=eps**2)[0]
