"""
pytest data/app_data/03-dl-training/01-optimizers/03-adam-bias-correction/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
update_moments = _module.update_moments
bias_correct = _module.bias_correct


def test_update_moments_matches_hand_computation():
    m, v = update_moments(0.0, 0.0, grad=5.0, beta1=0.9, beta2=0.999)
    assert np.isclose(m, 0.5)  # (1-0.9)*5
    assert np.isclose(v, 0.025)  # (1-0.999)*25


def test_update_moments_accumulates_over_multiple_steps():
    m, v = 0.0, 0.0
    for _ in range(3):
        m, v = update_moments(m, v, grad=2.0, beta1=0.9, beta2=0.999)
    assert m > 0.5  # should keep growing toward 2.0 with a constant gradient
    assert m < 2.0


def test_bias_correct_on_first_step_recovers_the_true_gradient():
    # The key demonstration: bias_correct on step 1 exactly cancels the
    # (1-beta) factor, recovering the true gradient value exactly.
    m, _ = update_moments(0.0, 0.0, grad=5.0, beta1=0.9, beta2=0.999)
    corrected = bias_correct(m, beta=0.9, t=1)
    assert np.isclose(corrected, 5.0)


def test_bias_correct_effect_shrinks_as_t_grows():
    m = 0.5  # some fixed raw moment value
    correction_factor_early = bias_correct(m, beta=0.9, t=1) / m
    correction_factor_late = bias_correct(m, beta=0.9, t=1000) / m
    assert correction_factor_early > correction_factor_late
    assert np.isclose(correction_factor_late, 1.0, atol=1e-3)


def test_bias_correct_matches_hand_computation():
    # moment=0.5, beta=0.9, t=2 -> 0.5 / (1 - 0.81) = 0.5/0.19
    result = bias_correct(0.5, beta=0.9, t=2)
    assert np.isclose(result, 0.5 / 0.19)


def test_update_moments_uses_squared_gradient_for_v_not_the_raw_gradient():
    m, v = update_moments(0.0, 0.0, grad=-3.0, beta1=0.9, beta2=0.999)
    # v uses grad^2 (always positive), m uses raw grad (keeps sign)
    assert m < 0.0
    assert v > 0.0
    assert np.isclose(v, 0.001 * 9.0)


def test_bias_correct_divides_not_multiplies_by_one_minus_beta_power():
    # Directly targets a mutant that multiplies by (1 - beta**t) instead
    # of dividing: on the first step, this would shrink the raw moment
    # further (wrong direction) instead of amplifying it correctly.
    m, _ = update_moments(0.0, 0.0, grad=5.0, beta1=0.9, beta2=0.999)
    result = bias_correct(m, beta=0.9, t=1)
    assert result > m  # correct correction always amplifies (divides by <1)
    assert np.isclose(result, 5.0)
