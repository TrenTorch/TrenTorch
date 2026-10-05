import numpy as np


def negative_sampling_loss(v_c, u_o, U_neg):
    v_c = np.asarray(v_c, dtype=float)
    pos = np.logaddexp(0.0, -(np.asarray(u_o, dtype=float) @ v_c))
    neg = np.logaddexp(0.0, np.asarray(U_neg, dtype=float) @ v_c).sum()
    return float(pos + neg)
