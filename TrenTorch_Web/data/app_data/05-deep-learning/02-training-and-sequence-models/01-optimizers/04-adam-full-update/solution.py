
import numpy as np

from _load import load_solution

update_moments = load_solution("dl-training-adam-bias-correction").update_moments
bias_correct = load_solution("dl-training-adam-bias-correction").bias_correct


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
    new_params = []
    new_m_list = []
    new_v_list = []
    for param, grad, m, v in zip(params, grads, m_list, v_list):
        m_new, v_new = update_moments(m, v, grad, beta1, beta2)
        m_hat = bias_correct(m_new, beta1, t)
        v_hat = bias_correct(v_new, beta2, t)
        param_new = param - lr * m_hat / (np.sqrt(v_hat) + eps)

        new_params.append(param_new)
        new_m_list.append(m_new)
        new_v_list.append(v_new)

    return new_params, new_m_list, new_v_list
