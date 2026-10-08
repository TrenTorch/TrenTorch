"""
pytest data/app_data/12-research-papers/01-optimization-and-training/01-adam/01-adam-moment-updates/tests.py
"""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adam-moment-updates")
adam_update_moments = _module.adam_update_moments


# ---- 1-2: basic correctness ----


def test_1_first_update_from_zero_state():
    m, v = adam_update_moments(0.0, 0.0, 2.0)
    assert math.isclose(m, 0.2)  # (1 - 0.9) * 2
    assert math.isclose(v, 0.004)  # (1 - 0.999) * 4


def test_2_moments_accumulate_over_two_steps():
    m, v = adam_update_moments(0.2, 0.004, 1.0)
    assert math.isclose(m, 0.9 * 0.2 + 0.1 * 1.0)
    assert math.isclose(v, 0.999 * 0.004 + 0.001 * 1.0)


# ---- shape / general-case coverage ----


def test_3_works_on_numpy_arrays():
    m, v = adam_update_moments(np.zeros(3), np.zeros(3), np.array([1.0, -2.0, 0.0]))
    np.testing.assert_allclose(m, [0.1, -0.2, 0.0])
    np.testing.assert_allclose(v, [0.001, 0.004, 0.0])


def test_4_custom_decay_rates_are_respected():
    m, v = adam_update_moments(0.0, 0.0, 1.0, beta1=0.5, beta2=0.25)
    assert math.isclose(m, 0.5)
    assert math.isclose(v, 0.75)


# ---- edge cases ----


def test_5_zero_gradient_decays_both_moments():
    m, v = adam_update_moments(1.0, 1.0, 0.0)
    assert math.isclose(m, 0.9)
    assert math.isclose(v, 0.999)


def test_6_negative_gradient_gives_positive_second_moment():
    _, v = adam_update_moments(0.0, 0.0, -3.0)
    assert v > 0


# ---- array hygiene ----


def test_7_does_not_mutate_inputs():
    m = np.array([0.5, 0.5])
    v = np.array([0.5, 0.5])
    grad = np.array([1.0, 1.0])
    adam_update_moments(m, v, grad)
    np.testing.assert_array_equal(m, [0.5, 0.5])
    np.testing.assert_array_equal(v, [0.5, 0.5])


# ---- mutation-catching ----


def test_8_second_moment_uses_square_not_absolute_value():
    _, v = adam_update_moments(0.0, 0.0, -3.0)
    assert math.isclose(v, 0.001 * 9)
    assert not math.isclose(v, 0.001 * 3)


def test_9_first_moment_keeps_sign_of_gradient():
    m, _ = adam_update_moments(0.0, 0.0, -2.0)
    assert math.isclose(m, -0.2)


# ---- independent oracle ----


def test_10_matches_a_hand_computed_reference_case():
    # m_1 = 0.9*0.1 + 0.1*(-4) = 0.09 - 0.4 = -0.31
    # v_1 = 0.999*0.5 + 0.001*16 = 0.4995 + 0.016 = 0.5155
    m, v = adam_update_moments(0.1, 0.5, -4.0)
    assert math.isclose(m, -0.31)
    assert math.isclose(v, 0.5155)
