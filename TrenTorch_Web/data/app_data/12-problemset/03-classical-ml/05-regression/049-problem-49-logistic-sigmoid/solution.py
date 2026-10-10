import numpy as np

def solve(x):
        x=np.asarray(x,float); out=np.empty_like(x); pos=x>=0; out[pos]=1/(1+np.exp(-x[pos])); ex=np.exp(x[~pos]); out[~pos]=ex/(1+ex); return out
