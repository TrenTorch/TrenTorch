import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

adam_step = load_solution("03-dl-training/01-optimizers/04-adam-full-update").adam_step


def save_checkpoint(params: list[np.ndarray], m_list: list[np.ndarray], v_list: list[np.ndarray], t: int) -> dict:
    """
    A checkpoint that saves EVERYTHING needed to resume training
    identically to an uninterrupted run: not just `params`, but also
    Adam's own per-parameter moving averages `m_list`/`v_list` and the
    step counter `t` (needed for Adam's bias correction).
    """
    pass


def train_n_steps(
    params: list[np.ndarray],
    m_list: list[np.ndarray],
    v_list: list[np.ndarray],
    t: int,
    grads_sequence: list[list[np.ndarray]],
    lr: float,
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], int]:
    """
    Runs `[03-dl-training/01-optimizers/04-adam-full-update]`'s
    `adam_step` once per entry in `grads_sequence`, threading `params`,
    `m_list`, `v_list`, and `t` through each successive call.
    """
    pass


def resume_from_full_checkpoint(
    checkpoint: dict, grads_sequence: list[list[np.ndarray]], lr: float
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], int]:
    """
    Resumes training from a FULL checkpoint (params AND optimizer
    state), continuing `grads_sequence` exactly as if training had never
    been interrupted.
    """
    pass


def resume_from_weights_only(
    params: list[np.ndarray], grads_sequence: list[list[np.ndarray]], lr: float
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], int]:
    """
    The WRONG way to resume: restores only `params`, and reinitializes
    `m_list`/`v_list` to zero and `t` to `1`, as if training were
    starting completely fresh, losing every bit of Adam's accumulated
    per-parameter history.
    """
    pass
