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
    new_params = []
    new_m_list = []
    new_v_list = []
    for param, grad, m, v in zip(params, grads, m_list, v_list):
        m_new, v_new = update_moments(m, v, grad, beta1, beta2)
        m_hat = bias_correct(m_new, beta1, t)
        v_hat = bias_correct(v_new, beta2, t)

        decayed_param = param - lr * weight_decay * param
        param_new = decayed_param - lr * m_hat / (np.sqrt(v_hat) + eps)

        new_params.append(param_new)
        new_m_list.append(m_new)
        new_v_list.append(v_new)

    return new_params, new_m_list, new_v_list
