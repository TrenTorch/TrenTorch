import numpy as np

def solve(control, treatment):
    """Implement a/b conversion rate according to the contract."""
    cr_a = np.mean(np.asarray(control, float))
    cr_b = np.mean(np.asarray(treatment, float))
    return (cr_a, cr_b, cr_b - cr_a)
