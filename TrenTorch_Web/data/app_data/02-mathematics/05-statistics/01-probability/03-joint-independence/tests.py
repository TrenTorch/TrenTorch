"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
joint_from_independent = _module.joint_from_independent
marginalize = _module.marginalize
is_independent = _module.is_independent
conditional_pmf_given_y = _module.conditional_pmf_given_y


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
