"""
pytest data/app_data/02-math-and-statistics/02-calculus/08-gradient-descent/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/02-calculus/08-gradient-descent")
gradient_descent_step = _module.gradient_descent_step
gradient_descent = _module.gradient_descent


# ---- 1-2: basic correctness ----


def test_1_single_step_on_a_scalar():
    result = gradient_descent_step(4.0, lambda x: 2 * x, 0.1)
    assert np.isclose(result, 3.2)  # 4 - 0.1*8


def test_2_full_loop_converges_toward_the_minimum_of_x_squared():
    trajectory = gradient_descent(4.0, lambda x: 2 * x, 0.1, 50)
    assert abs(trajectory[-1]) < 0.01


# ---- shape / general-case coverage ----


def test_3_trajectory_has_correct_length():
    trajectory = gradient_descent(1.0, lambda x: 2 * x, 0.1, 10)
    assert len(trajectory) == 11


def test_4_trajectory_starts_with_x0():
    trajectory = gradient_descent(5.0, lambda x: 2 * x, 0.1, 3)
    assert trajectory[0] == 5.0


def test_5_works_with_a_numpy_array_x():
    result = gradient_descent_step(np.array([2.0, 4.0]), lambda x: 2 * x, 0.1)
    np.testing.assert_allclose(result, [1.6, 3.2])


# ---- edge cases ----


def test_6_zero_steps_returns_only_x0():
    trajectory = gradient_descent(3.0, lambda x: 2 * x, 0.1, 0)
    assert trajectory == [3.0]


def test_7_zero_gradient_leaves_position_unchanged():
    result = gradient_descent_step(5.0, lambda x: 0.0, 0.1)
    assert result == 5.0


def test_8_negative_starting_position_still_descends():
    trajectory = gradient_descent(-4.0, lambda x: 2 * x, 0.1, 50)
    assert abs(trajectory[-1]) < 0.01


# ---- mutation-catching ----


def test_9_subtracts_gradient_not_adds_it():
    # A wrong implementation adding instead of subtracting would move
    # AWAY from the minimum, increasing the loss instead of decreasing it.
    trajectory = gradient_descent(4.0, lambda x: 2 * x, 0.1, 10)
    assert trajectory[-1] < trajectory[0]


def test_10_learning_rate_actually_scales_the_step():
    # A wrong implementation ignoring learning_rate (always subtracting
    # the raw gradient) would produce a very different result here.
    small_lr_result = gradient_descent_step(4.0, lambda x: 2 * x, 0.01)
    large_lr_result = gradient_descent_step(4.0, lambda x: 2 * x, 0.5)
    assert small_lr_result != large_lr_result
    assert np.isclose(small_lr_result, 3.92)
    assert np.isclose(large_lr_result, 0.0)


def test_11_each_step_uses_the_updated_position_not_the_original():
    # A wrong implementation recomputing every step from x0 instead of
    # the previous step's result would never actually converge properly.
    trajectory = gradient_descent(4.0, lambda x: 2 * x, 0.1, 3)
    # step1: 4 - 0.1*8 = 3.2; step2: 3.2 - 0.1*6.4 = 2.56; step3: 2.56 - 0.1*5.12 = 2.048
    np.testing.assert_allclose(trajectory, [4.0, 3.2, 2.56, 2.048], atol=1e-8)


# ---- independent oracle ----


def test_12_matches_a_hand_computed_reference_case():
    trajectory = gradient_descent(1.0, lambda x: 2 * x, 0.25, 2)
    # step1: 1 - 0.25*2 = 0.5; step2: 0.5 - 0.25*1 = 0.25
    np.testing.assert_allclose(trajectory, [1.0, 0.5, 0.25], atol=1e-10)
