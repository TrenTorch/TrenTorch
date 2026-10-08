import numpy as np


def implicit_reward(logp, ref, beta):
    """
    logp: log-probability of a response under the trained policy
    ref: log-probability of the same response under the reference model
    beta: KL strength

    Returns:
        The implicit reward beta * (logp - ref), element-wise.
    """
    # TODO: Scale the policy-to-reference log-ratio by beta (see Theory).
    pass
