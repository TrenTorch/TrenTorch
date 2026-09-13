import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

kl_divergence = load_solution("00-math-and-statistics/04-information-theory/03-kl-divergence").kl_divergence


def distillation_loss(teacher_probs: np.ndarray, student_probs: np.ndarray) -> float:
    """
    Knowledge distillation trains a (smaller) student to match a
    (larger) teacher's output distribution: minimizing
    KL(teacher || student) per example, averaged over the batch --
    exactly `math-kl-divergence`'s existing kl_divergence, applied
    once per (teacher_row, student_row) pair. Use base=np.e (natural
    log), the standard convention for this loss.
    """
    # TODO: for each (teacher_row, student_row) pair, compute
    # kl_divergence(teacher_row, student_row, base=np.e), then average
    # across all pairs.
    pass


def rlhf_kl_penalty(policy_probs: np.ndarray, reference_probs: np.ndarray, beta: float) -> float:
    """
    The KL penalty term real RLHF training adds to the reward: beta *
    KL(policy || reference), keeping the policy from drifting too far
    from the frozen reference model it started from -- the SAME
    kl_divergence formula distillation_loss uses, just applied to a
    policy/reference pair instead of a student/teacher pair, and
    scaled by beta.
    """
    # TODO: average kl_divergence(policy_row, reference_row, base=np.e)
    # over every row, then multiply by beta.
    pass
