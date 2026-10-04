import numpy as np

def solve(prior, likelihood_h1, likelihood_h0):
    """Implement bayes posterior according to the contract."""
    num = prior * likelihood_h1
    den = num + (1 - prior) * likelihood_h0
    return float(num / den)
