
import numpy as np

from _load import load_solution

kl_divergence = load_solution("math-kl-divergence").kl_divergence
softmax = load_solution("classification-softmax-cce").softmax
cce_loss = load_solution("classification-softmax-cce").cce_loss


def distillation_loss(
    student_logits: np.ndarray,
    teacher_logits: np.ndarray,
    true_labels: np.ndarray,
    temperature: float = 2.0,
    alpha: float = 0.5,
) -> float:
    """
    student_logits, teacher_logits: shape (batch_size, num_classes)
    true_labels: shape (batch_size,), integer class indices
    temperature: softens both distributions before comparing them (a
        higher temperature reveals more of the teacher's "dark
        knowledge" -- its relative confidence across ALL classes, not
        just the top one)
    alpha: how much weight to put on matching the teacher (soft loss)
        vs. getting the true label right (hard loss)

    Hinton et al.'s knowledge distillation loss: a weighted combination
    of (1) how well the student's temperature-softened distribution
    matches the teacher's, and (2) how well the student does on the
    actual hard labels.
    """
    # TODO:
    # 1. student_soft = softmax(student_logits / temperature),
    #    teacher_soft = softmax(teacher_logits / temperature).
    # 2. per_sample_kl: for each row i, kl_divergence(teacher_soft[i],
    #    student_soft[i], base=np.e) (natural log, matching how
    #    real distillation losses are usually reported).
    # 3. soft_loss = mean(per_sample_kl) * temperature**2 (the T^2
    #    factor is part of the original published formula -- it
    #    rescales the soft loss's gradient magnitude back to match the
    #    hard loss's, since dividing logits by T shrinks gradients by
    #    1/T^2).
    # 4. hard_loss = cce_loss(softmax(student_logits), true_labels)
    #    (ordinary cross-entropy against the true labels, at the
    #    ORIGINAL temperature of 1, not the softened one).
    # 5. return alpha * soft_loss + (1 - alpha) * hard_loss.
    pass
