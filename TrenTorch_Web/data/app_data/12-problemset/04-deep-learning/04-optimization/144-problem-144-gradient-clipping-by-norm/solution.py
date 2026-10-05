import numpy as np

def solve(grads, clip):
    """Global-norm clipping computes sqrt(sum_g sum(g^2)) and scales every gradient by min(1, clip/norm)."""
    gs=[np.asarray(g,dtype=float) for g in grads]; n=np.sqrt(sum(np.sum(g*g) for g in gs)); scale=min(1.0,clip/n) if n else 1.0; return [g*scale for g in gs]
