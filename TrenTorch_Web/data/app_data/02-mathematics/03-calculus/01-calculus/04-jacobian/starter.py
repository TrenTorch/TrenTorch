import numpy as np


def jacobian(f, x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """
    f: R^n -> R^m (takes a length-n vector, returns a length-m vector,
    or a scalar treated as m=1). Returns the (m, n) Jacobian matrix:

        J[i, j] = df_i / dx_j

    row i is output i's own gradient (02-partial-derivatives, applied
    per output), so column j of the Jacobian is exactly what varying
    x[j] alone (holding every other input fixed) does to every output
    at once. Use np.atleast_1d on f's return value so this works
    whether f returns a scalar or a vector.
    """
    pass
