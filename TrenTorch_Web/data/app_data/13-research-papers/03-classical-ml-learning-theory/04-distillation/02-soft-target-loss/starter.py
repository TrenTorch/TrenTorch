import numpy as np


def soft_target_ce(teacher_logits, student_logits, T):
    """
    teacher_logits: teacher class scores, shape (C,)
    student_logits: student class scores, shape (C,)
    T: distillation temperature

    Returns:
        The cross-entropy between the softened teacher and student distributions,
        multiplied by T**2, as a float.
    """
    # TODO: Soften both sets of logits, then compute -sum(p_teacher * log q_student) * T^2 (see Theory).
    pass
