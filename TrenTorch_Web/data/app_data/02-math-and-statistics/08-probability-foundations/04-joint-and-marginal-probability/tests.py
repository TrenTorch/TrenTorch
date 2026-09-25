"""
pytest data/app_data/02-math-and-statistics/08-probability-foundations/04-joint-and-marginal-probability/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/08-probability-foundations/04-joint-and-marginal-probability")
joint_from_independent = _module.joint_from_independent
marginalize = _module.marginalize


# ---- 1-2: basic correctness ----


def test_1_joint_of_two_fair_coins():
    result = joint_from_independent([0.5, 0.5], [0.5, 0.5])
    np.testing.assert_allclose(result, [[0.25, 0.25], [0.25, 0.25]])


def test_2_marginalizing_out_y_recovers_the_x_marginal():
    joint = joint_from_independent([0.2, 0.8], [0.5, 0.5])
    result = marginalize(joint, axis=1)
    np.testing.assert_allclose(result, [0.2, 0.8])


# ---- shape / general-case coverage ----


def test_3_joint_has_the_right_shape():
    result = joint_from_independent([0.2, 0.3, 0.5], [0.5, 0.5])
    assert result.shape == (3, 2)


def test_4_joint_sums_to_one():
    result = joint_from_independent([0.1, 0.2, 0.7], [0.4, 0.6])
    assert np.isclose(result.sum(), 1.0)


def test_5_marginalizing_out_x_recovers_the_y_marginal():
    marginal_y = [0.3, 0.7]
    joint = joint_from_independent([0.2, 0.8], marginal_y)
    result = marginalize(joint, axis=0)
    np.testing.assert_allclose(result, marginal_y)


# ---- edge cases ----


def test_6_deterministic_x_gives_a_joint_equal_to_y_marginal_on_one_row():
    # X is always x_0 (P=1), so joint[0,:] == marginal_y and joint[1,:] == 0
    result = joint_from_independent([1.0, 0.0], [0.4, 0.6])
    np.testing.assert_allclose(result[0], [0.4, 0.6])
    np.testing.assert_allclose(result[1], [0.0, 0.0])


def test_7_marginalizing_a_single_row_joint():
    joint = np.array([[0.3, 0.7]])
    result = marginalize(joint, axis=0)
    np.testing.assert_allclose(result, [0.3, 0.7])


# ---- array hygiene ----


def test_8_does_not_mutate_the_input_marginals():
    marginal_x = np.array([0.2, 0.8])
    marginal_y = np.array([0.5, 0.5])
    x_before = marginal_x.copy()
    y_before = marginal_y.copy()
    joint_from_independent(marginal_x, marginal_y)
    np.testing.assert_array_equal(marginal_x, x_before)
    np.testing.assert_array_equal(marginal_y, y_before)


# ---- mutation-catching ----


def test_9_joint_uses_multiplication_not_addition():
    # A wrong implementation adding instead of multiplying would give
    # 0.5+0.5=1.0 in every cell instead of 0.5*0.5=0.25.
    result = joint_from_independent([0.5, 0.5], [0.5, 0.5])
    assert np.isclose(result[0, 0], 0.25)
    assert not np.isclose(result[0, 0], 1.0)


def test_10_marginalize_sums_the_correct_axis():
    # A wrong implementation swapping axis=0 and axis=1 would return the
    # other marginal instead of the requested one.
    joint = joint_from_independent([0.1, 0.9], [0.4, 0.6])
    x_marginal = marginalize(joint, axis=1)
    y_marginal = marginalize(joint, axis=0)
    np.testing.assert_allclose(x_marginal, [0.1, 0.9])
    np.testing.assert_allclose(y_marginal, [0.4, 0.6])


# ---- independent oracle ----


def test_11_matches_a_hand_computed_reference_case():
    joint = joint_from_independent([0.25, 0.75], [0.6, 0.4])
    expected = np.array([[0.15, 0.1], [0.45, 0.3]])
    np.testing.assert_allclose(joint, expected, atol=1e-9)
    np.testing.assert_allclose(marginalize(joint, axis=1), [0.25, 0.75], atol=1e-9)
