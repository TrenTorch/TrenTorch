import numpy as np

def solve(eigenvalues):
    """The explained-variance share of component i is lambda_i / sum_j(lambda_j); shares sum to one when total variance is positive."""
    e=np.asarray(eigenvalues,dtype=float); total=e.sum(); return np.zeros_like(e) if total==0 else e/total
