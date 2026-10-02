"""
pytest tests.py
"""

import numpy as np
import math
from _load import load_solution

_module = load_solution(__file__)
marginal_x = _module.marginal_x
marginal_y = _module.marginal_y
conditional_x_given_y = _module.conditional_x_given_y
joint_via_chain_rule = _module.joint_via_chain_rule
chain_rule_general = _module.chain_rule_general
bayes_theorem = _module.bayes_theorem
posterior_binary = _module.posterior_binary


# A small joint distribution: rows are X in {0, 1}, columns are Y in {0, 1, 2}.
_JOINT = np.array(
    [
        [0.10, 0.20, 0.05],
        [0.15, 0.25, 0.25],
    ]
)


def test_marginal_x_sums_to_one():
    assert np.isclose(marginal_x(_JOINT).sum(), 1.0)


def test_marginal_y_sums_to_one():
    assert np.isclose(marginal_y(_JOINT).sum(), 1.0)


def test_marginal_x_matches_hand_computation():
    # row 0 sum: 0.10+0.20+0.05 = 0.35, row 1: 0.15+0.25+0.25 = 0.65
    result = marginal_x(_JOINT)
    assert np.allclose(result, [0.35, 0.65])


def test_marginal_y_matches_hand_computation():
    # col 0: 0.25, col 1: 0.45, col 2: 0.30
    result = marginal_y(_JOINT)
    assert np.allclose(result, [0.25, 0.45, 0.30])


def test_conditional_x_given_y_sums_to_one():
    result = conditional_x_given_y(_JOINT, y_index=1)
    assert np.isclose(result.sum(), 1.0)


def test_conditional_x_given_y_matches_hand_computation():
    # column 1: [0.20, 0.25], sum=0.45 -> normalized: [0.4444, 0.5556]
    result = conditional_x_given_y(_JOINT, y_index=1)
    assert np.allclose(result, [0.20 / 0.45, 0.25 / 0.45])


def test_conditional_x_given_y_for_each_y_value_all_sum_to_one():
    for y_index in range(_JOINT.shape[1]):
        result = conditional_x_given_y(_JOINT, y_index)
        assert np.isclose(result.sum(), 1.0)


def test_conditional_x_given_y_is_not_just_the_raw_unnormalized_column():
    # Directly targets a mutant that returns joint[:, y_index] directly
    # without dividing by its sum: the raw column here sums to 0.45, not 1.
    result = conditional_x_given_y(_JOINT, y_index=0)
    raw_column = _JOINT[:, 0]
    assert not np.isclose(result.sum(), raw_column.sum())
    assert np.isclose(result.sum(), 1.0)


def test_marginal_x_does_not_confuse_axis_with_marginal_y():
    # Directly targets a mutant that swaps axis=0 and axis=1 between the
    # two marginal functions: on a non-square joint table, this produces
    # a shape mismatch or a clearly wrong set of numbers.
    assert marginal_x(_JOINT).shape == (2,)
    assert marginal_y(_JOINT).shape == (3,)


# ---- 1-2: basic correctness ----


def test_1_three_variable_joint():
    result = joint_via_chain_rule(0.5, 0.4, 0.2)
    assert math.isclose(result, 0.04)


def test_2_general_chain_matches_the_three_variable_case():
    result = chain_rule_general([0.5, 0.4, 0.2])
    assert math.isclose(result, joint_via_chain_rule(0.5, 0.4, 0.2))


# ---- shape / general-case coverage ----


def test_3_general_chain_with_five_variables():
    conditionals = [0.9, 0.5, 0.5, 0.8, 0.3]
    expected = 0.9 * 0.5 * 0.5 * 0.8 * 0.3
    result = chain_rule_general(conditionals)
    assert math.isclose(result, expected)


def test_4_certain_first_variable_leaves_the_rest_unchanged():
    result = joint_via_chain_rule(1.0, 0.6, 0.7)
    assert math.isclose(result, 0.42)


# ---- edge cases ----


def test_5_single_variable_chain_is_just_its_own_probability():
    result = chain_rule_general([0.37])
    assert math.isclose(result, 0.37)


def test_6_any_zero_probability_factor_makes_the_whole_joint_zero():
    result = joint_via_chain_rule(0.5, 0.0, 0.9)
    assert result == 0.0


def test_7_all_probability_one_factors_give_a_joint_of_one():
    result = chain_rule_general([1.0, 1.0, 1.0])
    assert math.isclose(result, 1.0)


# ---- mutation-catching ----


def test_8_chain_rule_multiplies_not_adds():
    # A wrong implementation adding the factors would give 1.1 instead
    # of the correct 0.06 for these inputs.
    result = joint_via_chain_rule(0.5, 0.3, 0.4)
    assert math.isclose(result, 0.06)
    assert not math.isclose(result, 1.2)


def test_9_general_chain_uses_every_factor_not_just_the_first_and_last():
    # A wrong implementation multiplying only conditionals[0]*conditionals[-1]
    # would ignore the middle factor and give a different result.
    result = chain_rule_general([0.5, 0.2, 0.9])
    assert math.isclose(result, 0.09)
    assert not math.isclose(result, 0.45)


# ---- independent oracle ----


def test_10_matches_a_hand_computed_reference_case():
    # P(X)=0.6, P(Y|X)=0.3, P(Z|X,Y)=0.9 -> joint = 0.6*0.3*0.9 = 0.162
    result = joint_via_chain_rule(0.6, 0.3, 0.9)
    assert math.isclose(result, 0.162)
    assert math.isclose(chain_rule_general([0.6, 0.3, 0.9]), 0.162)


def test_bayes_theorem_matches_hand_computation():
    # prior=0.5, likelihood=0.8, evidence=0.4 -> (0.8*0.5)/0.4 = 1.0
    assert np.isclose(bayes_theorem(0.5, 0.8, 0.4), 1.0)


def test_bayes_theorem_with_certain_evidence_reduces_to_likelihood_times_prior():
    assert np.isclose(bayes_theorem(0.3, 0.6, 1.0), 0.18)


def test_posterior_binary_classic_disease_test_example():
    # Prevalence 1%, true positive rate 99%, false positive rate 5%.
    # Known counterintuitive result: posterior ~= 16.67%, not 99%.
    result = posterior_binary(prior_h=0.01, likelihood_e_given_h=0.99, likelihood_e_given_not_h=0.05)
    assert np.isclose(result, 0.99 * 0.01 / (0.99 * 0.01 + 0.05 * 0.99), atol=1e-6)
    assert result < 0.2


def test_posterior_binary_with_a_perfectly_reliable_test():
    # If the test never gives false positives, a positive result implies
    # certainty (posterior = 1.0), regardless of how rare the disease is.
    result = posterior_binary(prior_h=0.001, likelihood_e_given_h=1.0, likelihood_e_given_not_h=0.0)
    assert np.isclose(result, 1.0)


def test_posterior_binary_with_uninformative_evidence_does_not_change_belief():
    # If the evidence is equally likely whether H is true or false, it
    # carries no information, the posterior should equal the prior.
    result = posterior_binary(prior_h=0.3, likelihood_e_given_h=0.5, likelihood_e_given_not_h=0.5)
    assert np.isclose(result, 0.3)


def test_posterior_binary_increases_with_more_reliable_positive_evidence():
    weak_test = posterior_binary(prior_h=0.1, likelihood_e_given_h=0.6, likelihood_e_given_not_h=0.4)
    strong_test = posterior_binary(prior_h=0.1, likelihood_e_given_h=0.95, likelihood_e_given_not_h=0.05)
    assert strong_test > weak_test


def test_posterior_binary_computes_its_own_evidence_not_a_wrong_shortcut():
    # Directly targets a mutant that treats evidence as simply
    # likelihood_e_given_h (ignoring the "or H is false" branch of the
    # weighted sum entirely). For the disease example, using
    # evidence=0.99 directly (instead of the correctly weighted 0.0594)
    # would give posterior = 0.01, not the correct ~0.1667.
    result = posterior_binary(prior_h=0.01, likelihood_e_given_h=0.99, likelihood_e_given_not_h=0.05)
    assert not np.isclose(result, 0.01, atol=1e-3)
    assert np.isclose(result, 0.16666667, atol=1e-6)
