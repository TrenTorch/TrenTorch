import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

update_moments = load_solution("03-dl-training/01-optimizers/03-adam-bias-correction").update_moments
bias_correct = load_solution("03-dl-training/01-optimizers/03-adam-bias-correction").bias_correct


def adamw_step(
    params: list[np.ndarray],
    grads: list[np.ndarray],
    m_list: list[np.ndarray],
    v_list: list[np.ndarray],
    t: int,
    lr: float = 0.001,
    beta1: float = 0.9,
    beta2: float = 0.999,
    eps: float = 1e-8,
    weight_decay: float = 0.01,
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    """
    `Ridge Regression (L2)` (Classical ML) added its penalty directly
    into the LOSS, which is mathematically equivalent to adding
    `weight_decay * param` into the GRADIENT before it's used. Plain
    Adam applying L2 this way has a real, well-documented flaw: that
    decay term gets folded into m and v just like any other gradient
    signal, so it ends up scaled by Adam's own adaptive per-parameter
    denominator, weakening decay exactly where gradients have
    historically been large, the opposite of a clean, predictable
    weight-shrinkage effect.

    AdamW's fix, DECOUPLED weight decay: apply the shrinkage directly
    to the PARAMETER, entirely separately from the adaptive gradient
    update, so it always shrinks every parameter by the same
    predictable fraction, `lr * weight_decay`, regardless of that
    parameter's own gradient history.

        decayed_param = param - lr * weight_decay * param
        param_new     = decayed_param - lr * m_hat / (sqrt(v_hat) + eps)

    Reuses update_moments and bias_correct (already provided above)
    for the moment/bias-correction machinery, identical to
    Adam: full update rule's own approach.
    """
    pass
