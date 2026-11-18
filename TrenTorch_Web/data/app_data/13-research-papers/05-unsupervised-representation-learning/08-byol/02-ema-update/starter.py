import numpy as np


def ema_update(target, online, tau):
    """
    target: target network parameters
    online: online network parameters, same shape
    tau: moving-average rate in (0, 1]

    Returns:
        The updated target parameters, an exponential moving average of the online ones.
    """
    # TODO: Blend the target toward the online parameters with rate tau (see Theory).
    pass
