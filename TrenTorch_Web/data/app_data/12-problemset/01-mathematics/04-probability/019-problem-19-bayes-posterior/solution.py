import numpy as np

def solve(prior, likelihood_h1, likelihood_h0):
        num=prior*likelihood_h1
        den=num+(1-prior)*likelihood_h0
        return float(num/den)
