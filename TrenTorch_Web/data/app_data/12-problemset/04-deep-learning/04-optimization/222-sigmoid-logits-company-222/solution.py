import numpy as np

def solve(z):
    z=np.asarray(z,float)
    out=np.empty_like(z)
    pos=z>=0; out[pos]=1/(1+np.exp(-z[pos])); ez=np.exp(z[~pos]); out[~pos]=ez/(1+ez)
    return out
