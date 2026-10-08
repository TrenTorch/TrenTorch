import math


def reward_model_nll(y, r_a, r_b):
    """
    y: human label, 1 if A was preferred and 0 if B was preferred
    r_a: predicted reward of segment A
    r_b: predicted reward of segment B

    Returns:
        The negative log-likelihood of the label under the preference model, as a float.
    """
    # TODO: Compute the logistic preference probability and its log-likelihood for the label (see Theory).
    pass
