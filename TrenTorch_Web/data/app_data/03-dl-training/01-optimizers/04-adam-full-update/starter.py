import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

update_moments = load_solution("03-dl-training/01-optimizers/03-adam-bias-correction").update_moments
bias_correct = load_solution("03-dl-training/01-optimizers/03-adam-bias-correction").bias_correct


def adam_step(
    params: list[np.ndarray],
    grads: list[np.ndarray],
    m_list: list[np.ndarray],
    v_list: list[np.ndarray],
    t: int,
    lr: float = 0.001,
    beta1: float = 0.9,
    beta2: float = 0.999,
    eps: float = 1e-8,
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    """
    Assembles Adam's full update, one parameter at a time:

    1. Update both moments (Adam: bias-corrected moment estimates'
       update_moments, already provided above).
    2. Bias-correct both (bias_correct, already provided above),
       using `t` (the 1-indexed step count).
    3. Update the parameter using the CORRECTED moments:

           param_new = param - lr * m_hat / (sqrt(v_hat) + eps)

       `m_hat` (the corrected mean gradient) plays the role
       `SGD + Momentum`'s velocity played, driving the STEP DIRECTION.
       `sqrt(v_hat)` (the corrected root-mean-square gradient
       magnitude) divides that step, shrinking it for parameters whose
       gradients have been consistently LARGE, and allowing a
       relatively bigger step for parameters whose gradients have been
       consistently small, an ADAPTIVE, per-parameter learning rate.
       `eps` (tiny, e.g. 1e-8) exists purely to avoid dividing by
       exactly zero if v_hat ever collapses to 0.

    Returns (new_params, new_m_list, new_v_list), all as new lists.
    """
    pass
