import numpy as np


def annealing_cos(start: float, end: float, pct: float) -> float:
    return end + (start - end) / 2.0 * (1.0 + np.cos(np.pi * pct))


def onecycle_lr(
    step: int,
    total_steps: int,
    max_lr: float,
    pct_start: float = 0.3,
    div_factor: float = 25.0,
    final_div_factor: float = 1e4,
) -> float:
    initial_lr = max_lr / div_factor
    min_lr = initial_lr / final_div_factor
    step_up = pct_start * total_steps

    if step <= step_up:
        pct = step / step_up
        return annealing_cos(initial_lr, max_lr, pct)

    step_down = total_steps - step_up
    pct = min(1.0, (step - step_up) / step_down)
    return annealing_cos(max_lr, min_lr, pct)
