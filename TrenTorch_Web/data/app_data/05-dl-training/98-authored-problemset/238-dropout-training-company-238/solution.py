import numpy as np

def solve(x,p,seed=0):
    rng=np.random.default_rng(seed); x=np.asarray(x,float); mask=rng.random(x.shape)>=p; return x*mask/(1-p)
