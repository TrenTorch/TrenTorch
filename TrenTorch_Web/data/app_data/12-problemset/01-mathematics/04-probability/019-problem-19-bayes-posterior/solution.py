import numpy as np

def solve(prior, likelihood_h1, likelihood_h0):
    numerator = prior * likelihood_h1
    denominator = numerator + (1 - prior) * likelihood_h0
    return float(numerator / denominator)
