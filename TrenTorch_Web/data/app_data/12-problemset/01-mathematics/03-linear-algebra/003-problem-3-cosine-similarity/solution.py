import numpy as np

def solve(a, b):
        a, b = np.asarray(a, float), np.asarray(b, float)
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na == 0 or nb == 0: return 0.0
        return float(a @ b / (na * nb))
