import numpy as np

def solve(x, critical=1.96):
    """Implement confidence interval for mean according to the contract."""
    x = np.asarray(x, float)
    se = np.std(x, ddof=1) / np.sqrt(len(x))
    m = x.mean()
    return (m - critical * se, m + critical * se)
