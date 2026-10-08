import numpy as np


def mu_law_encode(x, mu=255):
    """
    x: audio samples in [-1, 1]
    mu: companding parameter (255 in WaveNet)

    Returns:
        The mu-law companded signal, sign(x) * ln(1 + mu |x|) / ln(1 + mu), in [-1, 1].
    """
    # TODO: Apply the mu-law compression from Theory element-wise.
    pass
