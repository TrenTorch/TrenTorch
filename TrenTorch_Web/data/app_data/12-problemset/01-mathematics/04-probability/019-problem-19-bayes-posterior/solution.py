import numpy as np

def solve(prior, likelihood_h1, likelihood_h0):
    for v in (prior, likelihood_h1, likelihood_h0):
        if not 0 <= v <= 1:
            raise ValueError("prior and likelihoods must lie in [0, 1]")
    num = prior * likelihood_h1
    den = num + (1 - prior) * likelihood_h0
    if den == 0:
        raise ValueError("evidence is zero: posterior is undefined")
    return float(num / den)
