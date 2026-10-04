import numpy as np

def solve(intra, nearest):
    """For a point, a is its average within-cluster distance and b is the closest competing-cluster distance; s=(b-a)/max(a,b), with s=0 when both are zero."""
    a=float(np.mean(intra)); b=float(np.min(nearest)); d=max(a,b); return 0.0 if d==0 else (b-a)/d
