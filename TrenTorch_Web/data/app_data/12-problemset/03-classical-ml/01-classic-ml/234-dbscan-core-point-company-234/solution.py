import numpy as np

def solve(X,eps,min_samples):
    X=np.asarray(X,float); D=((X[:,None,:]-X[None,:,:])**2).sum(axis=2)**0.5; return (D<=eps).sum(axis=1)>=min_samples
