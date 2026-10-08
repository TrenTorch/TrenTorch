import numpy as np


def lars_update(w, g, lr, eta, wd):
    """
    w: layer weights; g: layer gradient; lr: global learning rate
    eta: trust coefficient; wd: weight decay

    Returns:
        The weights after one LARS step, where the update is scaled by the layer's trust ratio.
    """
    # TODO: Scale the decayed gradient by lr times the trust ratio and subtract from w (see Theory).
    pass
