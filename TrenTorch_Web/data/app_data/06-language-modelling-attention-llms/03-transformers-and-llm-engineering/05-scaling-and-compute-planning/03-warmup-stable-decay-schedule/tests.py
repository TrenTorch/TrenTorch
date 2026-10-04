"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
wsd_lr = _module.wsd_lr
ARGS = dict(peak_lr=1.0, warmup_steps=10, decay_start=80, total_steps=100, final_ratio=0.1)


def test_1_warmup_is_linear_and_reaches_peak():
    assert np.isclose(wsd_lr(0, **ARGS), 0.1) and np.isclose(wsd_lr(9, **ARGS), 1.0)


def test_2_plateau_is_flat():
    assert all(wsd_lr(s, **ARGS) == 1.0 for s in (10, 40, 79))


def test_3_decay_hand_computed():
    assert np.isclose(wsd_lr(90, **ARGS), 1.0 - 0.5 * 0.9)
    assert np.isclose(wsd_lr(80, **ARGS), 1.0)


def test_4_ends_at_final_ratio_and_stays_there():
    assert np.isclose(wsd_lr(100, **ARGS), 0.1) and np.isclose(wsd_lr(500, **ARGS), 0.1)


def test_5_monotone_after_peak():
    vals = [wsd_lr(s, **ARGS) for s in range(9, 101)]
    assert all(a >= b - 1e-12 for a, b in zip(vals, vals[1:]))


def test_6_schedule_before_decay_does_not_depend_on_total_steps():
    a = dict(ARGS, total_steps=100)
    b = dict(ARGS, total_steps=10_000)
    assert all(wsd_lr(s, **a) == wsd_lr(s, **b) for s in range(0, 80))


def test_7_degenerate_phases():
    assert wsd_lr(5, 2.0, 0, 5, 5, 0.5) == 1.0
    assert wsd_lr(3, 2.0, 0, 10, 10, 1.0) == 2.0
