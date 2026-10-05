import numpy as np

def solve(precision, recall):
    p, r = precision, recall
    return 0.0 if p + r == 0 else float(2 * p * r / (p + r))
