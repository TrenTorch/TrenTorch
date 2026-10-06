import numpy as np

def solve(x, B=1000, alpha=0.05, seed=0):
        rng=np.random.default_rng(seed); x=np.asarray(x,float); means=np.empty(B)
        for i in range(B): means[i]=np.mean(rng.choice(x,len(x),replace=True))
        return float(np.quantile(means,alpha/2)), float(np.quantile(means,1-alpha/2))
