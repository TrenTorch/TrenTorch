
import numpy as np

from _load import load_solution

kl_divergence = load_solution("math-kl-divergence").kl_divergence


def distillation_loss(teacher_probs: np.ndarray, student_probs: np.ndarray) -> float:
    per_example = np.array(
        [kl_divergence(t, s, base=np.e) for t, s in zip(teacher_probs, student_probs)]
    )
    return float(per_example.mean())


def rlhf_kl_penalty(policy_probs: np.ndarray, reference_probs: np.ndarray, beta: float) -> float:
    per_token = np.array(
        [kl_divergence(p, r, base=np.e) for p, r in zip(policy_probs, reference_probs)]
    )
    return float(beta * per_token.mean())
