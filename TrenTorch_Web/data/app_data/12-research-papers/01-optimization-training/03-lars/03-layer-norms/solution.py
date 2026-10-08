import numpy as np


def layer_norms(layers):
    return [float(np.linalg.norm(w)) for w in layers]
