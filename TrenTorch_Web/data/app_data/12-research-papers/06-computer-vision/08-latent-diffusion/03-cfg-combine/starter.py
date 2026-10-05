import numpy as np


def cfg_combine(eps_u, eps_c, w):
    """
    eps_u: noise prediction without the text condition
    eps_c: noise prediction with the text condition
    w: guidance strength (w = 0 ignores the condition; larger pushes harder toward it)

    Returns:
        The guided noise prediction eps_u + w * (eps_c - eps_u).
    """
    # TODO: Extrapolate from the unconditional prediction toward the conditional one (see Theory).
    pass
