import numpy as np

def solve(lr0, min_lr, t, T):
    """Cosine decay interpolates from lr0 to min_lr with a half cosine: min_lr+0.5*(lr0-min_lr)*(1+cos(pi*t/T))."""
    lr0=float(lr0); min_lr=float(min_lr); T=int(T); t=min(max(int(t),0),T); progress=1.0 if T<=0 else t/T; return float(min_lr+0.5*(lr0-min_lr)*(1+np.cos(np.pi*progress)))
