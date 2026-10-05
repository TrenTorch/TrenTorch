import numpy as np


def cfg_combine(eps_uncond, eps_cond, w):
    u = np.asarray(eps_uncond, dtype=float)
    return u + w * (np.asarray(eps_cond, dtype=float) - u)


def drop_condition(cond_ids, p, null_id, rng):
    ids = np.array(cond_ids, copy=True)
    u = rng.random_sample(len(ids))
    ids[u < p] = null_id
    return ids
