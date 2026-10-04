import numpy as np

def solve(lr0, gamma, t):
    """Exponential decay multiplies the initial rate by gamma once per step: lr_t=lr0*gamma^t."""
    return lr0*(gamma**t)
