import numpy as np

def solve(f, x, h=1e-5):
    return float((f(x + h) - f(x - h)) / (2 * h))
