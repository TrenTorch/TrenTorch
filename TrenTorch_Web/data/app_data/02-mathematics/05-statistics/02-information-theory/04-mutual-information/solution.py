
import numpy as np

from _load import load_solution

_cond_prob = load_solution("math-conditional-probability")
marginal_x = _cond_prob.marginal_x
marginal_y = _cond_prob.marginal_y

kl_divergence = load_solution("math-kl-divergence").kl_divergence


def mutual_information(joint: np.ndarray, base: float = 2.0) -> float:
    px = marginal_x(joint)
    py = marginal_y(joint)
    independent_joint = np.outer(px, py)
    return kl_divergence(joint.flatten(), independent_joint.flatten(), base)
