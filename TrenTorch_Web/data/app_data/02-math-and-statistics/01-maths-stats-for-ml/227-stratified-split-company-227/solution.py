import numpy as np

def solve(y,val_fraction,seed=0):
    y=np.asarray(y); rng=np.random.default_rng(seed); train=[]; val=[]
    for c in np.unique(y):
        idx=np.flatnonzero(y==c); rng.shuffle(idx); k=int(round(len(idx)*val_fraction)); val.extend(idx[:k]); train.extend(idx[k:])
    return np.array(sorted(train)),np.array(sorted(val))
