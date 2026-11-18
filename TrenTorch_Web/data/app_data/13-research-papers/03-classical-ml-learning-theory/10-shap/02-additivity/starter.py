import numpy as np


def additivity_gap(phi, f_x, f_base):
    """
    phi: attribution per feature, shape (n,)
    f_x: model output for the explained input
    f_base: model output for the baseline

    Returns:
        sum(phi) - (f_x - f_base). Zero means the attributions are additive
        and complete, as SHAP requires.
    """
    # TODO: Compare the sum of the attributions with the output difference (see Theory).
    pass
