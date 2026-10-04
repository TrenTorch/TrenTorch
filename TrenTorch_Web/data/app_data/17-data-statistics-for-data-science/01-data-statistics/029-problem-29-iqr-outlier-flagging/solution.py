import numpy as np

def solve(x):
    """Implement iqr outlier flagging according to the contract."""
    x = np.asarray(x, float)
    q1, q3 = np.quantile(x, [0.25, 0.75])
    iqr = q3 - q1
    return (x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)
