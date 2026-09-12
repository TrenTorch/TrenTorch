"""
pytest data/app_data/03-dl-training/01-optimizers/09-onecyclelr/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
annealing_cos = _module.annealing_cos
onecycle_lr = _module.onecycle_lr


def test_annealing_cos_at_pct_zero_returns_start():
    assert np.isclose(annealing_cos(0.1, 0.9, 0.0), 0.1)


def test_annealing_cos_at_pct_one_returns_end():
    assert np.isclose(annealing_cos(0.1, 0.9, 1.0), 0.9)


def test_annealing_cos_at_pct_half_returns_the_midpoint():
    assert np.isclose(annealing_cos(0.1, 0.9, 0.5), 0.5)


def test_annealing_cos_works_when_start_is_greater_than_end():
    assert np.isclose(annealing_cos(0.9, 0.1, 0.0), 0.9)
    assert np.isclose(annealing_cos(0.9, 0.1, 1.0), 0.1)
    assert np.isclose(annealing_cos(0.9, 0.1, 0.5), 0.5)


def test_onecycle_starts_at_initial_lr():
    result = onecycle_lr(0, total_steps=100, max_lr=0.01, pct_start=0.3, div_factor=25.0, final_div_factor=1e4)
    expected_initial_lr = 0.01 / 25.0
    assert np.isclose(result, expected_initial_lr)


def test_onecycle_reaches_max_lr_exactly_at_step_up():
    step_up = 0.3 * 100
    result = onecycle_lr(step_up, total_steps=100, max_lr=0.01, pct_start=0.3, div_factor=25.0, final_div_factor=1e4)
    assert np.isclose(result, 0.01)


def test_onecycle_reaches_min_lr_exactly_at_total_steps():
    result = onecycle_lr(100, total_steps=100, max_lr=0.01, pct_start=0.3, div_factor=25.0, final_div_factor=1e4)
    expected_min_lr = (0.01 / 25.0) / 1e4
    assert np.isclose(result, expected_min_lr, atol=1e-12)


def test_onecycle_hand_computed_midpoint_of_rising_phase():
    # step_up = 30, so step 15 is halfway through the rising phase -> midpoint
    # between initial_lr and max_lr.
    result = onecycle_lr(15, total_steps=100, max_lr=0.01, pct_start=0.3, div_factor=25.0, final_div_factor=1e4)
    initial_lr = 0.01 / 25.0
    expected = (initial_lr + 0.01) / 2.0
    assert np.isclose(result, expected)


def test_onecycle_hand_computed_midpoint_of_falling_phase():
    # step_up = 30, step_down = 70, so step 65 is halfway through the falling
    # phase -> midpoint between max_lr and min_lr.
    result = onecycle_lr(65, total_steps=100, max_lr=0.01, pct_start=0.3, div_factor=25.0, final_div_factor=1e4)
    min_lr = (0.01 / 25.0) / 1e4
    expected = (0.01 + min_lr) / 2.0
    assert np.isclose(result, expected, atol=1e-9)


def test_onecycle_min_lr_is_far_below_initial_lr():
    initial_lr = 0.01 / 25.0
    min_lr = initial_lr / 1e4
    assert min_lr < initial_lr / 1000.0


def test_onecycle_is_monotonically_increasing_during_rising_phase():
    step_up = 30
    lrs = [
        onecycle_lr(s, total_steps=100, max_lr=0.01, pct_start=0.3, div_factor=25.0, final_div_factor=1e4)
        for s in range(0, step_up + 1)
    ]
    assert all(lrs[i] <= lrs[i + 1] for i in range(len(lrs) - 1))


def test_onecycle_is_monotonically_decreasing_during_falling_phase():
    step_up = 30
    lrs = [
        onecycle_lr(s, total_steps=100, max_lr=0.01, pct_start=0.3, div_factor=25.0, final_div_factor=1e4)
        for s in range(step_up, 101)
    ]
    assert all(lrs[i] >= lrs[i + 1] for i in range(len(lrs) - 1))


def test_onecycle_uses_max_lr_not_initial_lr_as_the_falling_phase_start():
    # Directly targets a mutant that starts the falling phase from
    # initial_lr instead of max_lr (e.g. by reusing the wrong variable),
    # which would make the falling phase barely move at all since
    # initial_lr and min_lr are already close in scale compared to max_lr.
    result = onecycle_lr(31, total_steps=100, max_lr=0.01, pct_start=0.3, div_factor=25.0, final_div_factor=1e4)
    initial_lr = 0.01 / 25.0
    # Just after the peak, the LR must be very close to max_lr, not close
    # to initial_lr.
    assert abs(result - 0.01) < abs(result - initial_lr)
