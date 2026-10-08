import numpy as np


def soft_update(target, online, tau):
    target = np.asarray(target, dtype=float)
    online = np.asarray(online, dtype=float)
    return (1 - tau) * target + tau * online
