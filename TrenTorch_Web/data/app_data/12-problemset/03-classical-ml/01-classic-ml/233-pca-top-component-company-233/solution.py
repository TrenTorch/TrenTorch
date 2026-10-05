import numpy as np

def solve(X):
    X=np.asarray(X,float); Z=X-X.mean(axis=0); C=np.cov(Z,rowvar=False,bias=True); w,V=np.linalg.eigh(C); v=V[:,-1]; v=v/np.linalg.norm(v); return v if v[np.argmax(np.abs(v))]>=0 else -v
