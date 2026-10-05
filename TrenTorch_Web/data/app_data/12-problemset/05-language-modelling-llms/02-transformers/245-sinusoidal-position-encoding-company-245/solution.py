import numpy as np

def solve(n,d):
    P=np.zeros((n,d)); pos=np.arange(n)[:,None]; i=np.arange(0,d,2); div=np.exp(-np.log(10000)*i/d); P[:,0::2]=np.sin(pos*div); P[:,1::2]=np.cos(pos*div[:len(P[:,1::2].T)]); return P
