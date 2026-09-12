import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

adam_step = load_solution("03-dl-training/01-optimizers/04-adam-full-update").adam_step


def save_checkpoint(params: list[np.ndarray], m_list: list[np.ndarray], v_list: list[np.ndarray], t: int) -> dict:
    return dict(
        params=[p.copy() for p in params],
        m_list=[m.copy() for m in m_list],
        v_list=[v.copy() for v in v_list],
        t=t,
    )


def train_n_steps(
    params: list[np.ndarray],
    m_list: list[np.ndarray],
    v_list: list[np.ndarray],
    t: int,
    grads_sequence: list[list[np.ndarray]],
    lr: float,
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], int]:
    for grads in grads_sequence:
        params, m_list, v_list = adam_step(params, grads, m_list, v_list, t, lr=lr)
        t += 1
    return params, m_list, v_list, t


def resume_from_full_checkpoint(
    checkpoint: dict, grads_sequence: list[list[np.ndarray]], lr: float
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], int]:
    return train_n_steps(
        checkpoint["params"], checkpoint["m_list"], checkpoint["v_list"], checkpoint["t"], grads_sequence, lr
    )


def resume_from_weights_only(
    params: list[np.ndarray], grads_sequence: list[list[np.ndarray]], lr: float
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], int]:
    m_list = [np.zeros_like(p) for p in params]
    v_list = [np.zeros_like(p) for p in params]
    return train_n_steps(params, m_list, v_list, 1, grads_sequence, lr)
