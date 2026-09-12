import numpy as np


def linear_warmup_lr(step: int, warmup_steps: int, base_lr: float) -> float:
    return base_lr * min(1.0, step / warmup_steps)


def cosine_decay_lr(step: int, total_steps: int, base_lr: float, min_lr: float = 0.0) -> float:
    progress = min(1.0, step / total_steps)
    return min_lr + 0.5 * (base_lr - min_lr) * (1.0 + np.cos(np.pi * progress))


def warmup_cosine_lr(
    step: int, warmup_steps: int, total_steps: int, base_lr: float, min_lr: float = 0.0
) -> float:
    if step < warmup_steps:
        return linear_warmup_lr(step, warmup_steps, base_lr)
    decay_step = step - warmup_steps
    decay_total_steps = total_steps - warmup_steps
    return cosine_decay_lr(decay_step, decay_total_steps, base_lr, min_lr)
