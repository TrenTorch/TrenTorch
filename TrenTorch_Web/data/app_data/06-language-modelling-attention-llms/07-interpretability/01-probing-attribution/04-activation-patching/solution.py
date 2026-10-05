import numpy as np


def patch_rows(clean, corrupt, rows):
    out = np.array(corrupt, dtype=float, copy=True)
    rows = list(rows)
    out[rows] = np.asarray(clean, dtype=float)[rows]
    return out


def recovery(clean_metric, corrupt_metric, patched_metric):
    return float((patched_metric - corrupt_metric) / (clean_metric - corrupt_metric))


def patching_scan(model, clean, corrupt):
    m_clean, m_corrupt = model(clean), model(corrupt)
    T = np.asarray(clean).shape[0]
    return np.array([recovery(m_clean, m_corrupt, model(patch_rows(clean, corrupt, [t]))) for t in range(T)])
