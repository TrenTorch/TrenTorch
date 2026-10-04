import numpy as np

def solve(logits,p_cut,rng):
        z=np.asarray(logits,float); z=z-z.max(); p=np.exp(z); p/=p.sum(); order=np.argsort(-p); cs=np.cumsum(p[order]); keep=order[cs<=p_cut]; keep=np.r_[keep,order[min(len(order)-1,np.searchsorted(cs,p_cut))]]; q=np.zeros_like(p); q[keep]=p[keep]; q/=q.sum(); return rng.choice(len(z),p=q)
