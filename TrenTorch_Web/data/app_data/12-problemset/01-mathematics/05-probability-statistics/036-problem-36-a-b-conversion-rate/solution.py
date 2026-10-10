import numpy as np

def solve(control, treatment):
    control = np.asarray(control, dtype=float)
    treatment = np.asarray(treatment, dtype=float)
    for g in (control, treatment):
        if g.ndim != 1 or g.size == 0 or not np.all((g == 0) | (g == 1)):
            raise ValueError("control and treatment must be non-empty 1-D sequences of 0/1 outcomes")
    cr_a = float(np.mean(control))
    cr_b = float(np.mean(treatment))
    return cr_a, cr_b, cr_b - cr_a
