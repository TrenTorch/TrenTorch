import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

_cond_prob = load_solution("00-math-and-statistics/03-probability/04-conditional-probability")
marginal_x = _cond_prob.marginal_x
marginal_y = _cond_prob.marginal_y

kl_divergence = load_solution("00-math-and-statistics/04-information-theory/03-kl-divergence").kl_divergence


def mutual_information(joint: np.ndarray, base: float = 2.0) -> float:
    px = marginal_x(joint)
    py = marginal_y(joint)
    independent_joint = np.outer(px, py)
    return kl_divergence(joint.flatten(), independent_joint.flatten(), base)
