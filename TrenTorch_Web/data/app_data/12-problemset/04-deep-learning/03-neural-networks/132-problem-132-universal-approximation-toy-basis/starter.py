import numpy as np

def solve(X, y, knots):
    """The fixed ReLU basis has columns max(X_i-knot_j,0); least squares chooses weights minimizing the squared residual to y."""
    pass
