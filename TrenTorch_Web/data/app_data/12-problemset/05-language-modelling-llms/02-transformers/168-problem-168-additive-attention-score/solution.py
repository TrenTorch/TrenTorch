import numpy as np

def solve(Q,K,V,mask=None):
        return np.tanh(np.asarray(Q)@Wq + np.asarray(K)@Wk).sum(-1)
