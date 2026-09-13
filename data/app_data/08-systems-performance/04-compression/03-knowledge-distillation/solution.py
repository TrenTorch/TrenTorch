import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

kl_divergence = load_solution("00-math-and-statistics/04-information-theory/03-kl-divergence").kl_divergence
softmax = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax
cce_loss = load_solution("01-classical-ml/02-classification/06-softmax-cce").cce_loss


def distillation_loss(
    student_logits: np.ndarray,
    teacher_logits: np.ndarray,
    true_labels: np.ndarray,
    temperature: float = 2.0,
    alpha: float = 0.5,
) -> float:
    student_soft = softmax(student_logits / temperature)
    teacher_soft = softmax(teacher_logits / temperature)

    per_sample_kl = [
        kl_divergence(teacher_soft[i], student_soft[i], base=np.e) for i in range(len(teacher_soft))
    ]
    soft_loss = float(np.mean(per_sample_kl)) * temperature**2

    hard_loss = cce_loss(softmax(student_logits), true_labels)

    return alpha * soft_loss + (1.0 - alpha) * hard_loss
