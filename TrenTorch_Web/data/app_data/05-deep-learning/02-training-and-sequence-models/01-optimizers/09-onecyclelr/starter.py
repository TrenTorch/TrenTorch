import numpy as np


def annealing_cos(start: float, end: float, pct: float) -> float:
    """
    Interpolates smoothly from `start` to `end` as `pct` goes from 0 to 1,
    using a cosine curve (zero slope at both ends). See Theory for the
    exact formula.
    """
    pass


def onecycle_lr(
    step: int,
    total_steps: int,
    max_lr: float,
    pct_start: float = 0.3,
    div_factor: float = 25.0,
    final_div_factor: float = 1e4,
) -> float:
    """
    The one-cycle learning rate policy: anneal UP from a low initial_lr to
    max_lr over the first `pct_start` fraction of training, then anneal
    DOWN from max_lr to an even lower min_lr over the rest of training.

        initial_lr = max_lr / div_factor
        min_lr = initial_lr / final_div_factor

    Use `annealing_cos` (already provided above) for both phases.
    """
    pass
