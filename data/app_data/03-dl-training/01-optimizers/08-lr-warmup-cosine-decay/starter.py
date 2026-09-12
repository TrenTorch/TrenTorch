import numpy as np


def linear_warmup_lr(step: int, warmup_steps: int, base_lr: float) -> float:
    """
    Ramps the learning rate linearly from 0 up to base_lr over the
    first `warmup_steps` steps, then holds at base_lr afterward.
    """
    pass


def cosine_decay_lr(step: int, total_steps: int, base_lr: float, min_lr: float = 0.0) -> float:
    """
    Decays the learning rate smoothly from base_lr down to min_lr,
    following one half-period of a cosine curve, reaching min_lr
    exactly at `total_steps` and staying there afterward.

        progress = min(1, step / total_steps)
        lr = min_lr + 0.5 * (base_lr - min_lr) * (1 + cos(pi * progress))
    """
    pass


def warmup_cosine_lr(
    step: int, warmup_steps: int, total_steps: int, base_lr: float, min_lr: float = 0.0
) -> float:
    """
    Combines both schedules: linear_warmup_lr for the first
    `warmup_steps` steps (already provided above), then cosine_decay_lr
    (also provided above) for the remaining steps, re-based so the
    decay phase itself starts counting from 0 at the moment warmup ends.
    """
    pass
