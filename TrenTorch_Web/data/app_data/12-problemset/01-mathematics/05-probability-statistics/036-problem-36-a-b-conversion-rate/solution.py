import numpy as np

def solve(control, treatment):
    control = np.asarray(control, dtype=float)
    treatment = np.asarray(treatment, dtype=float)
    rate_control = float(np.mean(control))
    rate_treatment = float(np.mean(treatment))
    return rate_control, rate_treatment, rate_treatment - rate_control
