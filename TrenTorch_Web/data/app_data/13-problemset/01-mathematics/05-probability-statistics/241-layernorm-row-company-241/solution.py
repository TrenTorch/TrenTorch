import numpy as np

def solve(X,gamma,beta,eps=1e-5):
    X=np.asarray(X,float); m=X.mean(axis=-1,keepdims=True); v=((X-m)**2).mean(axis=-1,keepdims=True); return gamma*(X-m)/np.sqrt(v+eps)+beta
