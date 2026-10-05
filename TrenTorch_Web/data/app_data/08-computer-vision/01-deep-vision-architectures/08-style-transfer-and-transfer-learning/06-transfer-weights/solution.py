import numpy as np


def transfer_weights(src, dst):
    new_dst, copied, skipped = {}, [], []
    for name, value in dst.items():
        if name in src and np.shape(src[name]) == np.shape(value):
            new_dst[name] = np.array(src[name], copy=True)
            copied.append(name)
        else:
            new_dst[name] = np.array(value, copy=True)
            skipped.append(name)
    return new_dst, sorted(copied), sorted(skipped)
