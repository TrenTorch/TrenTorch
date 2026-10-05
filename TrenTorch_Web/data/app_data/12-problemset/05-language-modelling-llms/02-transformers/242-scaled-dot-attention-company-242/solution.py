import numpy as np

def solve(Q,K,V):
    Q=np.asarray(Q,float); K=np.asarray(K,float); V=np.asarray(V,float); d=Q.shape[-1]; S=Q@K.T/np.sqrt(d); S=np.where(np.triu(np.ones(S.shape),1).astype(bool),-np.inf,S); P=np.exp(S-np.max(S,axis=1,keepdims=True)); P=P/P.sum(axis=1,keepdims=True); return P@V
