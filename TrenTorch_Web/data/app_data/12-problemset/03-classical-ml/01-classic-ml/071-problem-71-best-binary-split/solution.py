import numpy as np

def solve(x,y):
        x=np.asarray(x); y=np.asarray(y); best=None
        for t in np.unique(x)[:-1]:
            L=y[x<=t]; R=y[x>t]
            if len(L)==0 or len(R)==0: continue
            def g(z):
                _,c=np.unique(z,return_counts=True); p=c/len(z); return 1-np.sum(p*p)
            score=len(L)/len(y)*g(L)+len(R)/len(y)*g(R)
            if best is None or score<best[0]: best=(score,t)
        return best
