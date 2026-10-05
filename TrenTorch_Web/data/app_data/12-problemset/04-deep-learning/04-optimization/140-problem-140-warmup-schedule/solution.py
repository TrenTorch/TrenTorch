import numpy as np

def solve(lr0, min_lr, t, warmup, T):
    """Warmup grows linearly for the first warmup steps, then the rate follows a cosine decay from lr0 to min_lr by step T."""
    if t<warmup: return lr0*(t+1)/warmup
    q=min(t-warmup,max(1,T-warmup)); return min_lr+0.5*(lr0-min_lr)*(1+np.cos(np.pi*q/max(1,T-warmup)))
