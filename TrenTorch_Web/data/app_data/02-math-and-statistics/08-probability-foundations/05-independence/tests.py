"""
pytest data/app_data/02-math-and-statistics/08-probability-foundations/05-independence/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/08-probability-foundations/05-independence")
is_independent = _module.is_independent
conditional_pmf_given_y = _module.conditional_pmf_given_y


# ---- 1-2: basic correctness ----


def test_1_two_fair_independent_coins():
    joint = np.array([[0.25, 0.25], [0.25, 0.25]])
    assert is_independent(joint) is True


def test_2_conditional_pmf_of_a_dependent_joint():
    # joint[0,:]=[0.4,0.0], joint[1,:]=[0.1,0.5] -- given Y=0, only X=0 or X=1 possible
    joint = np.array([[0.4, 0.0], [0.1, 0.5]])
    result = conditional_pmf_given_y(joint, y_index=0)
    np.testing.assert_allclose(result, [0.8, 0.2])  # 0.4/0.5, 0.1/0.5


# ---- shape / general-case coverage ----


def test_3_a_dependent_joint_is_correctly_flagged_as_not_independent():
    # X and Y perfectly correlated: only (0,0) and (1,1) have mass.
    joint = np.array([[0.5, 0.0], [0.0, 0.5]])
    assert is_independent(joint) is False


def test_4_independence_holds_for_unequal_marginals():
    marginal_x = np.array([0.3, 0.7])
    marginal_y = np.array([0.6, 0.4])
    joint = np.outer(marginal_x, marginal_y)
    assert is_independent(joint) is True


def test_5_conditional_pmf_sums_to_one():
    joint = np.array([[0.1, 0.2, 0.0], [0.3, 0.1, 0.3]])
    for j in range(3):
        result = conditional_pmf_given_y(joint, y_index=j)
        assert np.isclose(result.sum(), 1.0)


# ---- edge cases ----


def test_6_deterministic_relationship_between_x_and_y_is_not_independent():
    joint = np.array([[0.5, 0.0], [0.0, 0.5]])
    assert is_independent(joint, tol=1e-9) is False


def test_7_a_single_row_joint_is_trivially_independent():
    # Only one possible X value -- X carries no information, so any Y
    # distribution is independent of it.
    joint = np.array([[0.2, 0.3, 0.5]])
    assert is_independent(joint) is True


# ---- mutation-catching ----


def test_8_is_independent_checks_the_full_outer_product_not_just_one_cell():
    # A wrong implementation checking only joint[0,0] against the
    # marginals' product would wrongly pass this joint (which agrees at
    # [0,0] but not elsewhere).
    joint = np.array([[0.16, 0.24], [0.24, 0.36]])  # actually independent
    dependent = np.array([[0.16, 0.34], [0.24, 0.26]])  # matches at [0,0] only
    assert is_independent(joint) is True
    assert is_independent(dependent) is False


def test_9_conditional_pmf_divides_by_marginal_y_not_marginal_x():
    # A wrong implementation dividing by the X marginal instead of Y's
    # would give a different (and non-normalized) result.
    joint = np.array([[0.3, 0.1], [0.3, 0.3]])
    result = conditional_pmf_given_y(joint, y_index=1)
    np.testing.assert_allclose(result, [0.25, 0.75])  # 0.1/0.4, 0.3/0.4


# ---- independent oracle ----


def test_10_matches_a_hand_computed_reference_case():
    marginal_x = np.array([0.2, 0.5, 0.3])
    marginal_y = np.array([0.4, 0.6])
    joint = np.outer(marginal_x, marginal_y)
    assert is_independent(joint) is True
    result = conditional_pmf_given_y(joint, y_index=0)
    np.testing.assert_allclose(result, marginal_x, atol=1e-9)
