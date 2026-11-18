import numpy as np

def solve(X,i,eps,min_samples=1):
        X=np.asarray(X,float); d=np.sum((X-X[i])**2,axis=1); return int(np.sum(d<=eps**2)>=min_samples)
